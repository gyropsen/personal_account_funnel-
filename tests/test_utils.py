import pytest

from src.utils import check_trigger


@pytest.mark.asyncio
async def test_check_trigger():
    assert await check_trigger("ожИдать")
    assert await check_trigger("прекрАсно")
    assert not await check_trigger("как дела?")
