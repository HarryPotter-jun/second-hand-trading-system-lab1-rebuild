"""高 DPI WebView 桌面壳：为校园二手集市提供原生手机 App 风格的本地 UI。"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import webview

from market_service import BusinessError, MarketService, ProductStatus, Roles, User


class MarketApi:
    """暴露给本地页面的最小业务 API；所有写操作仍由 MarketService 校验。"""

    def __init__(self) -> None:
        self.service = MarketService(str(Path(__file__).with_name("market.db")))
        self.user: Optional[User] = None

    def _user(self) -> User:
        if self.user is None:
            raise BusinessError("请先登录。")
        return self.user

    @staticmethod
    def _ok(data=None) -> dict:
        return {"ok": True, "data": data}

    @staticmethod
    def _fail(error: Exception) -> dict:
        return {"ok": False, "message": str(error)}

    def login(self, phone: str, password: str) -> dict:
        try:
            self.user = self.service.login(phone, password)
            return self._ok(self.me())
        except BusinessError as error:
            return self._fail(error)

    def register(self, phone: str, nickname: str, password: str, role: str) -> dict:
        try:
            self.user = self.service.register(phone, nickname, password, role)
            return self._ok(self.me())
        except BusinessError as error:
            return self._fail(error)

    def update_nickname(self, nickname: str) -> dict:
        try:
            self.user = self.service.update_nickname(self._user(), nickname)
            return self._ok(self.me())
        except BusinessError as error:
            return self._fail(error)

    def me(self) -> dict:
        if self.user is None:
            return {}
        return {"id": self.user.id, "name": self.user.nickname, "role": self.user.role}

    def logout(self) -> dict:
        self.user = None
        return self._ok()

    def products(self, keyword: str = "", category: str = "全部", status: str = "全部") -> dict:
        try:
            rows = self.service.products(self.user, keyword, category, status)
            return self._ok([dict(row) for row in rows])
        except BusinessError as error:
            return self._fail(error)

    def product(self, product_id: int) -> dict:
        try:
            return self._ok(dict(self.service.product(product_id, self._user())))
        except BusinessError as error:
            return self._fail(error)

    def reserve(self, product_id: int, version: int) -> dict:
        try:
            self.service.reserve(self._user(), product_id, version)
            return self._ok()
        except BusinessError as error:
            return self._fail(error)

    def favorite(self, product_id: int) -> dict:
        try:
            return self._ok(self.service.toggle_favorite(self._user(), product_id))
        except BusinessError as error:
            return self._fail(error)

    def favorites(self) -> dict:
        try:
            return self._ok([dict(row) for row in self.service.favorites(self._user())])
        except BusinessError as error:
            return self._fail(error)

    def orders(self) -> dict:
        try:
            return self._ok([dict(row) for row in self.service.reservations_for(self._user())])
        except BusinessError as error:
            return self._fail(error)

    def seller_products(self) -> dict:
        try:
            return self._ok([dict(row) for row in self.service.seller_products(self._user())])
        except BusinessError as error:
            return self._fail(error)

    def seller_orders(self) -> dict:
        try:
            return self._ok(
                [dict(row) for row in self.service.reservations_for(self._user(), received=True)]
            )
        except BusinessError as error:
            return self._fail(error)

    def create_product(self, fields: dict, submit: bool) -> dict:
        try:
            product_id = self.service.create_product(self._user(), fields, submit)
            return self._ok({"id": product_id})
        except BusinessError as error:
            return self._fail(error)

    def update_product(self, product_id: int, fields: dict) -> dict:
        try:
            self.service.update_product(self._user(), product_id, fields)
            return self._ok()
        except BusinessError as error:
            return self._fail(error)

    def off_shelf(self, product_id: int) -> dict:
        try:
            self.service.off_shelf(self._user(), product_id)
            return self._ok()
        except BusinessError as error:
            return self._fail(error)

    def cancel_reservation(self, reservation_id: int) -> dict:
        try:
            self.service.cancel_or_reject(self._user(), reservation_id)
            return self._ok()
        except BusinessError as error:
            return self._fail(error)

    def reject_reservation(self, reservation_id: int) -> dict:
        try:
            self.service.cancel_or_reject(self._user(), reservation_id, reject=True)
            return self._ok()
        except BusinessError as error:
            return self._fail(error)

    def confirm_reservation(self, reservation_id: int) -> dict:
        try:
            self.service.confirm_reservation(self._user(), reservation_id)
            return self._ok()
        except BusinessError as error:
            return self._fail(error)

    def confirm_delivery(self, reservation_id: int) -> dict:
        try:
            self.service.confirm_delivery(self._user(), reservation_id)
            return self._ok()
        except BusinessError as error:
            return self._fail(error)

    def confirm_receipt(self, reservation_id: int) -> dict:
        try:
            self.service.confirm_receipt(self._user(), reservation_id)
            return self._ok()
        except BusinessError as error:
            return self._fail(error)

    def report_product(self, product_id: int, reason: str) -> dict:
        try:
            self.service.report(self._user(), product_id, reason)
            return self._ok()
        except BusinessError as error:
            return self._fail(error)

    def reports(self) -> dict:
        try:
            return self._ok([dict(row) for row in self.service.reports(self._user())])
        except BusinessError as error:
            return self._fail(error)

    def handle_report(self, report_id: int, violation: bool, reason: str) -> dict:
        try:
            self.service.handle_report(self._user(), report_id, violation, reason)
            return self._ok()
        except BusinessError as error:
            return self._fail(error)

    def review_product(self, product_id: int, approved: bool, reason: str = "") -> dict:
        try:
            self.service.review_product(self._user(), product_id, approved, reason)
            return self._ok()
        except BusinessError as error:
            return self._fail(error)

    def admin(self) -> dict:
        try:
            user = self._user()
            return self._ok({
                "stats": self.service.statistics(user),
                "logs": [dict(row) for row in self.service.logs(user)[:8]],
                "pending": [
                    dict(row)
                    for row in self.service.products(user, status=ProductStatus.PENDING)
                ],
            })
        except BusinessError as error:
            return self._fail(error)


def main() -> None:
    root = Path(__file__).resolve().parent
    window = webview.create_window(
        "集市 · 校园二手交易", (root / "ui" / "index.html").as_uri(), js_api=MarketApi(),
        width=1240, height=820, min_size=(980, 700), background_color="#f4f6fb",
    )
    webview.start(debug=False)


if __name__ == "__main__":
    main()
