import logging
from anthropic import Anthropic
from django.conf import settings

logger = logging.getLogger(__name__)


def estimate_item_value(item_id: int) -> None:
    """
    Called by django-q as a background task.
    Asks Claude to estimate the current market value of a collection item
    and writes it back to current_value if not already set.
    """
    # Import here to avoid circular imports at module load time
    from .models import CollectionItem

    try:
        item = CollectionItem.objects.get(pk=item_id)
    except CollectionItem.DoesNotExist:
        logger.warning(f"estimate_item_value: item {item_id} not found")
        return

    # Skip if the user already supplied a value
    if item.current_value is not None:
        return

    client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    prompt = f"""You are a collectibles market expert. Based on the details below, estimate the current secondary market value of this item in USD.

Item details:
- Name: {item.name}
- Version / Edition: {item.version or 'N/A'}
- Manufacturer: {item.manufacturer or 'N/A'}
- Originating property / franchise: {item.originating_property or 'N/A'}
- Condition: {item.get_status_display()}
- Description: {item.description or 'N/A'}

Respond with a JSON object and nothing else. Use this exact shape:
{{"estimated_value": <number>, "confidence": "low" | "medium" | "high", "reasoning": "<one sentence>"}}

If you cannot make a reasonable estimate, set estimated_value to null."""

    try:
        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}],
        )

        import json
        raw = message.content[0].text.strip()
        data = json.loads(raw)

        estimated = data.get("estimated_value")
        if estimated is not None:
            item.current_value = round(float(estimated), 2)
            item.save(update_fields=["current_value"])
            logger.info(
                f"estimate_item_value: set current_value={item.current_value} "
                f"for item {item_id} (confidence={data.get('confidence')})"
            )
        else:
            logger.info(f"estimate_item_value: Claude could not estimate value for item {item_id}")

    except Exception as e:
        logger.error(f"estimate_item_value: failed for item {item_id} — {e}")