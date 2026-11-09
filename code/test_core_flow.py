"""不依赖界面的核心业务流程自检。"""

from pathlib import Path

from market_service import (
    BusinessError,
    MarketService,
    ProductStatus,
    ReservationStatus,
)


def main() -> None:
    database = Path(__file__).with_name("test_market.db")
    if database.exists():
        database.unlink()
    service = MarketService(str(database))
    buyer = service.login("13800000001", "buyer123")
    seller = service.login("13800000002", "seller123")
    admin = service.login("13800000003", "admin123")

    product = service.products(buyer, category="数码")[0]
    original_version = product["version"]
    service.reserve(buyer, product["id"], original_version)
    reserved = service.product(product["id"], buyer)
    assert reserved["status"] == ProductStatus.RESERVED
    try:
        service.reserve(buyer, product["id"], original_version)
        raise AssertionError("旧版本预约请求应被拒绝")
    except BusinessError:
        pass

    reservation = service.reservations_for(seller, received=True)[0]
    assert reservation["status"] == ReservationStatus.PENDING
    service.confirm_reservation(seller, reservation["id"])
    service.confirm_delivery(seller, reservation["id"])
    service.confirm_receipt(buyer, reservation["id"])
    sold = service.product(product["id"], buyer)
    assert sold["status"] == ProductStatus.SOLD

    review_item = [item for item in service.products(admin) if item["status"] == ProductStatus.PENDING][0]
    service.review_product(admin, review_item["id"], True)
    approved = service.product(review_item["id"], admin)
    assert approved["status"] == ProductStatus.ON_SALE
    assert len(service.logs(admin)) >= 8

    seller_product = service.create_product(
        seller,
        {
            "title": "可编辑的宿舍书架",
            "description": "九成新，尺寸适合宿舍桌面。",
            "category": "生活",
            "condition": "9成新",
            "price": "80",
            "delivery": "校内自取",
            "icon": "🗄️",
        },
        submit=False,
    )
    service.update_product(
        seller,
        seller_product,
        {
            "title": "可编辑的宿舍书架（已更新）",
            "description": "九成新，尺寸适合宿舍桌面，支持当面验货。",
            "category": "生活",
            "condition": "9成新",
            "price": "88",
            "delivery": "校内自取",
            "icon": "🗄️",
        },
    )
    edited = service.product(seller_product, seller)
    assert edited["title"].endswith("已更新）")
    assert edited["status"] == ProductStatus.DRAFT

    favorite_product = service.products(buyer, category="图书")[0]
    assert service.toggle_favorite(buyer, favorite_product["id"]) is True
    assert service.toggle_favorite(buyer, favorite_product["id"]) is False
    service.report(buyer, favorite_product["id"], "商品描述需要管理员进一步核验。")
    report = [item for item in service.reports(admin) if item["product_id"] == favorite_product["id"]][0]
    service.handle_report(admin, report["id"], False, "未发现违反平台规则的情况。")
    assert [item for item in service.reports(admin) if item["id"] == report["id"]][0]["status"] == "已驳回"

    sale_product = [
        item
        for item in service.products(buyer, category="生活")
        if item["status"] == ProductStatus.ON_SALE
    ][0]
    service.off_shelf(seller, sale_product["id"])
    assert service.product(sale_product["id"], admin)["status"] == ProductStatus.OFF_SHELF
    try:
        service.product(sale_product["id"], buyer)
        raise AssertionError("普通用户不应查看已下架商品")
    except BusinessError:
        pass

    nickname = service.update_nickname(buyer, "阿明同学")
    assert nickname.nickname == "阿明同学"
    database.unlink()
    print("核心交易、商品管理、收藏、举报与权限流程自检通过。")


if __name__ == "__main__":
    main()
