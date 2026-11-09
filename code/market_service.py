"""校园二手集市的领域服务与 SQLite 持久化层。"""

from __future__ import annotations

import hashlib
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


class BusinessError(Exception):
    """用户可见的业务规则错误。"""


class Roles:
    BUYER = "买家"
    SELLER = "卖家"
    ADMIN = "管理员"


class ProductStatus:
    DRAFT = "草稿"
    PENDING = "待审核"
    ON_SALE = "在售"
    RESERVED = "已预约"
    SOLD = "已售出"
    OFF_SHELF = "已下架"
    VIOLATION = "违规下架"


class ReservationStatus:
    PENDING = "待确认"
    CONFIRMED = "已确认"
    CANCELLED = "已取消"
    REJECTED = "已拒绝"
    FINISHED = "已完成"


@dataclass(frozen=True)
class User:
    id: int
    phone: str
    nickname: str
    role: str


class MarketService:
    """实现 UML 类图中的认证、商品、预约、收藏、举报、日志和统计服务。"""

    def __init__(self, database_path: str) -> None:
        self.database_path = database_path
        self.initialize()

    @contextmanager
    def transaction(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    @staticmethod
    def _now() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _digest(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def initialize(self) -> None:
        Path(self.database_path).parent.mkdir(parents=True, exist_ok=True)
        with self.transaction() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phone TEXT NOT NULL UNIQUE,
                    nickname TEXT NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('买家', '卖家', '管理员')),
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    seller_id INTEGER NOT NULL REFERENCES users(id),
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    category TEXT NOT NULL,
                    condition_text TEXT NOT NULL,
                    price REAL NOT NULL,
                    image_icon TEXT NOT NULL,
                    delivery_method TEXT NOT NULL,
                    status TEXT NOT NULL,
                    version INTEGER NOT NULL DEFAULT 1,
                    published_at TEXT NOT NULL,
                    review_reason TEXT DEFAULT '',
                    violation_reason TEXT DEFAULT ''
                );
                CREATE TABLE IF NOT EXISTS reservations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER NOT NULL REFERENCES products(id),
                    buyer_id INTEGER NOT NULL REFERENCES users(id),
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    seller_delivered_at TEXT,
                    buyer_received_at TEXT
                );
                CREATE TABLE IF NOT EXISTS favorites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    buyer_id INTEGER NOT NULL REFERENCES users(id),
                    product_id INTEGER NOT NULL REFERENCES products(id),
                    created_at TEXT NOT NULL,
                    UNIQUE(buyer_id, product_id)
                );
                CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    reporter_id INTEGER NOT NULL REFERENCES users(id),
                    product_id INTEGER NOT NULL REFERENCES products(id),
                    reason TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT '待处理',
                    handler_id INTEGER REFERENCES users(id),
                    result TEXT DEFAULT '',
                    created_at TEXT NOT NULL,
                    handled_at TEXT
                );
                CREATE TABLE IF NOT EXISTS operation_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operator_id INTEGER REFERENCES users(id),
                    action TEXT NOT NULL,
                    object_type TEXT NOT NULL,
                    object_id INTEGER,
                    result TEXT NOT NULL,
                    reason TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                """
            )
        self.seed_demo_data()

    def log(
        self,
        conn: sqlite3.Connection,
        user_id: Optional[int],
        action: str,
        object_type: str,
        object_id: Optional[int],
        result: str,
        reason: str = "",
    ) -> None:
        conn.execute(
            """INSERT INTO operation_logs
               (operator_id, action, object_type, object_id, result, reason, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (user_id, action, object_type, object_id, result, reason, self._now()),
        )

    def seed_demo_data(self) -> None:
        with self.transaction() as conn:
            count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
            if count:
                return
            users = [
                ("13800000001", "阿明", "buyer123", Roles.BUYER),
                ("13800000002", "小柯", "seller123", Roles.SELLER),
                ("13800000003", "胡老师", "admin123", Roles.ADMIN),
                ("13800000004", "阿澈", "buyer123", Roles.BUYER),
                ("13800000005", "骑行社", "seller123", Roles.SELLER),
            ]
            for phone, name, password, role in users:
                conn.execute(
                    """INSERT INTO users(phone, nickname, password_hash, role, created_at)
                       VALUES (?, ?, ?, ?, ?)""",
                    (phone, name, self._digest(password), role, self._now()),
                )
            products = [
                (2, "iPad Air 5 95新 深空灰 64G", "自用一学期，无磕碰，屏幕贴膜，附原装充电线。", "数码", "95新", 2399, "💻", "校内自取", ProductStatus.ON_SALE),
                (2, "民谣吉他 入门款 赠琴包", "练习用吉他，音色正常，赠送琴包与调音器。", "生活", "9成新", 329, "🎸", "校内自取", ProductStatus.ON_SALE),
                (2, "算法导论 第三版 中文版", "教材保存良好，少量笔记，适合课程学习。", "图书", "99新", 68, "📖", "邮寄", ProductStatus.ON_SALE),
                (5, "捷安特通勤自行车 已上锁", "车况良好，可现场验车，附车锁。", "运动", "8成新", 580, "🚲", "校内自取", ProductStatus.ON_SALE),
                (5, "演唱会门票两张（代排）", "转让两张门票，请联系确认场次信息。", "票券", "全新", 1800, "🎫", "校内自取", ProductStatus.PENDING),
            ]
            for item in products:
                conn.execute(
                    """INSERT INTO products
                       (seller_id, title, description, category, condition_text, price,
                        image_icon, delivery_method, status, published_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (*item, self._now()),
                )
            conn.execute(
                """INSERT INTO reports(reporter_id, product_id, reason, created_at)
                   VALUES (1, 5, '疑似违规代拍，需要平台审核。', ?)""",
                (self._now(),),
            )

    def register(self, phone: str, nickname: str, password: str, role: str) -> User:
        if not phone.isdigit() or len(phone) != 11:
            raise BusinessError("手机号必须为 11 位数字。")
        if not nickname.strip():
            raise BusinessError("用户名不能为空。")
        if len(password) < 8:
            raise BusinessError("密码至少需要 8 位。")
        if role not in (Roles.BUYER, Roles.SELLER):
            raise BusinessError("仅支持注册买家或卖家账号。")
        with self.transaction() as conn:
            exists = conn.execute("SELECT 1 FROM users WHERE phone = ?", (phone,)).fetchone()
            if exists:
                self.log(conn, None, "注册", "用户", None, "失败", "手机号已注册")
                raise BusinessError("该手机号已注册，请直接登录。")
            cursor = conn.execute(
                """INSERT INTO users(phone, nickname, password_hash, role, created_at)
                   VALUES (?, ?, ?, ?, ?)""",
                (phone, nickname.strip(), self._digest(password), role, self._now()),
            )
            self.log(conn, cursor.lastrowid, "注册", "用户", cursor.lastrowid, "成功")
            return User(cursor.lastrowid, phone, nickname.strip(), role)

    def login(self, phone: str, password: str) -> User:
        with self.transaction() as conn:
            row = conn.execute(
                "SELECT * FROM users WHERE phone = ? AND password_hash = ?",
                (phone, self._digest(password)),
            ).fetchone()
            if row is None:
                self.log(conn, None, "登录", "用户", None, "失败", "手机号或密码错误")
                raise BusinessError("手机号或密码错误。")
            self.log(conn, row["id"], "登录", "用户", row["id"], "成功")
            return User(row["id"], row["phone"], row["nickname"], row["role"])

    def update_nickname(self, user: User, nickname: str) -> User:
        """用户可以修改非唯一的公开昵称。"""

        if not nickname.strip():
            raise BusinessError("用户名不能为空。")
        with self.transaction() as conn:
            conn.execute(
                "UPDATE users SET nickname = ? WHERE id = ?",
                (nickname.strip(), user.id),
            )
            self.log(conn, user.id, "修改用户名", "用户", user.id, "成功")
        return User(user.id, user.phone, nickname.strip(), user.role)

    def products(
        self,
        user: Optional[User],
        keyword: str = "",
        category: str = "全部",
        status: str = "全部",
    ) -> list[sqlite3.Row]:
        clauses, values = [], []
        if not user or user.role != Roles.ADMIN:
            clauses.append("p.status NOT IN (?, ?)")
            values.extend((ProductStatus.OFF_SHELF, ProductStatus.VIOLATION))
        if keyword.strip():
            clauses.append("(p.title LIKE ? OR p.description LIKE ?)")
            values.extend((f"%{keyword.strip()}%", f"%{keyword.strip()}%"))
        if category != "全部":
            clauses.append("p.category = ?")
            values.append(category)
        if status != "全部":
            clauses.append("p.status = ?")
            values.append(status)
        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        with self.transaction() as conn:
            return conn.execute(
                f"""SELECT p.*, u.nickname AS seller_name FROM products p
                    JOIN users u ON u.id = p.seller_id {where}
                    ORDER BY p.id DESC""",
                values,
            ).fetchall()

    def product(self, product_id: int, user: Optional[User]) -> sqlite3.Row:
        with self.transaction() as conn:
            row = conn.execute(
                """SELECT p.*, u.nickname AS seller_name FROM products p
                   JOIN users u ON u.id = p.seller_id WHERE p.id = ?""",
                (product_id,),
            ).fetchone()
            if row is None:
                raise BusinessError("商品不存在。")
            hidden = row["status"] in (ProductStatus.OFF_SHELF, ProductStatus.VIOLATION)
            if hidden and (not user or user.role != Roles.ADMIN):
                raise BusinessError("该商品当前不可查看。")
            if row["status"] == ProductStatus.RESERVED and (
                not user or user.role != Roles.ADMIN
            ):
                reservation = conn.execute(
                    """SELECT 1 FROM reservations WHERE product_id = ? AND buyer_id = ?
                       AND status IN (?, ?)""",
                    (
                        product_id,
                        user.id,
                        ReservationStatus.PENDING,
                        ReservationStatus.CONFIRMED,
                    ),
                ).fetchone()
                if row["seller_id"] != user.id and reservation is None:
                    raise BusinessError("该商品已预约，仅交易双方可查看详情。")
            return row

    def create_product(self, seller: User, fields: dict[str, str], submit: bool) -> int:
        self._require_role(seller, Roles.SELLER)
        required = ("title", "description", "category", "condition", "price", "delivery")
        if submit and any(not fields.get(key, "").strip() for key in required):
            raise BusinessError("请完整填写标题、描述、分类、成色、价格和取货方式。")
        try:
            price = float(fields.get("price", "0"))
        except ValueError as error:
            raise BusinessError("价格必须是数字。") from error
        if price <= 0 or price > 1_000_000:
            raise BusinessError("价格必须大于 0 且不超过 1,000,000 元。")
        with self.transaction() as conn:
            if submit:
                duplicate = conn.execute(
                    """SELECT 1 FROM products
                       WHERE seller_id = ? AND title = ? AND price = ? AND description = ?
                       AND datetime(published_at) >= datetime('now', '-60 seconds')""",
                    (seller.id, fields["title"].strip(), price, fields["description"].strip()),
                ).fetchone()
                if duplicate:
                    raise BusinessError("60 秒内不能重复提交相同商品。")
            status = ProductStatus.PENDING if submit else ProductStatus.DRAFT
            cursor = conn.execute(
                """INSERT INTO products
                   (seller_id, title, description, category, condition_text, price,
                    image_icon, delivery_method, status, published_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    seller.id, fields["title"].strip(), fields["description"].strip(),
                    fields["category"].strip(), fields["condition"].strip(), price,
                    fields.get("icon", "📦"), fields["delivery"].strip(), status, self._now(),
                ),
            )
            action = "提交商品审核" if submit else "保存商品草稿"
            self.log(conn, seller.id, action, "商品", cursor.lastrowid, "成功")
            return cursor.lastrowid

    def seller_products(self, seller: User) -> list[sqlite3.Row]:
        self._require_role(seller, Roles.SELLER)
        with self.transaction() as conn:
            return conn.execute(
                "SELECT * FROM products WHERE seller_id = ? ORDER BY id DESC", (seller.id,)
            ).fetchall()

    def update_product(self, seller: User, product_id: int, fields: dict[str, str]) -> None:
        """编辑草稿、待审核或在售商品；待审核编辑后仍需重新审核。"""

        self._require_role(seller, Roles.SELLER)
        required = ("title", "description", "category", "condition", "price", "delivery")
        if any(not fields.get(key, "").strip() for key in required):
            raise BusinessError("请完整填写标题、描述、分类、成色、价格和取货方式。")
        try:
            price = float(fields["price"])
        except ValueError as error:
            raise BusinessError("价格必须是数字。") from error
        if price <= 0 or price > 1_000_000:
            raise BusinessError("价格必须大于 0 且不超过 1,000,000 元。")
        with self.transaction() as conn:
            item = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
            if item is None or item["seller_id"] != seller.id:
                raise BusinessError("无权编辑该商品。")
            if item["status"] not in (ProductStatus.DRAFT, ProductStatus.PENDING, ProductStatus.ON_SALE):
                raise BusinessError("已预约、已售出或已下架商品不能编辑关键信息。")
            target_status = ProductStatus.PENDING if item["status"] == ProductStatus.PENDING else item["status"]
            conn.execute(
                """UPDATE products SET title = ?, description = ?, category = ?, condition_text = ?,
                   price = ?, image_icon = ?, delivery_method = ?, status = ?, version = version + 1
                   WHERE id = ?""",
                (
                    fields["title"].strip(), fields["description"].strip(), fields["category"].strip(),
                    fields["condition"].strip(), price, fields.get("icon", item["image_icon"]),
                    fields["delivery"].strip(), target_status, product_id,
                ),
            )
            self.log(conn, seller.id, "编辑商品", "商品", product_id, "成功")

    def off_shelf(self, seller: User, product_id: int) -> None:
        """卖家下架在售商品。"""

        self._require_role(seller, Roles.SELLER)
        with self.transaction() as conn:
            item = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
            if item is None or item["seller_id"] != seller.id:
                raise BusinessError("无权下架该商品。")
            if item["status"] != ProductStatus.ON_SALE:
                raise BusinessError("仅在售商品可以下架；已预约商品请先处理预约。")
            conn.execute(
                """UPDATE products SET status = ?, version = version + 1 WHERE id = ?""",
                (ProductStatus.OFF_SHELF, product_id),
            )
            self.log(conn, seller.id, "下架商品", "商品", product_id, "成功")

    def review_product(self, admin: User, product_id: int, approved: bool, reason: str = "") -> None:
        self._require_role(admin, Roles.ADMIN)
        with self.transaction() as conn:
            item = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
            if item is None or item["status"] != ProductStatus.PENDING:
                raise BusinessError("仅能审核待审核商品。")
            if not approved and not reason.strip():
                raise BusinessError("驳回审核时必须填写原因。")
            target = ProductStatus.ON_SALE if approved else ProductStatus.DRAFT
            conn.execute(
                """UPDATE products SET status = ?, review_reason = ?, version = version + 1
                   WHERE id = ?""",
                (target, "" if approved else reason.strip(), product_id),
            )
            self.log(conn, admin.id, "商品审核", "商品", product_id, "成功", reason.strip())

    def reserve(self, buyer: User, product_id: int, expected_version: int) -> None:
        self._require_role(buyer, Roles.BUYER)
        with self.transaction() as conn:
            item = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
            if item is None:
                raise BusinessError("商品不存在。")
            if item["seller_id"] == buyer.id:
                raise BusinessError("不能预约自己发布的商品。")
            if item["status"] != ProductStatus.ON_SALE or item["version"] != expected_version:
                self.log(conn, buyer.id, "发起预约", "商品", product_id, "失败", "状态或版本冲突")
                raise BusinessError("商品状态已变化，请刷新后再试。")
            active = conn.execute(
                """SELECT 1 FROM reservations WHERE product_id = ?
                   AND status IN (?, ?)""",
                (product_id, ReservationStatus.PENDING, ReservationStatus.CONFIRMED),
            ).fetchone()
            if active:
                raise BusinessError("该商品已经被预约。")
            updated = conn.execute(
                """UPDATE products SET status = ?, version = version + 1
                   WHERE id = ? AND status = ? AND version = ?""",
                (ProductStatus.RESERVED, product_id, ProductStatus.ON_SALE, expected_version),
            ).rowcount
            if updated != 1:
                raise BusinessError("商品状态已变化，请刷新后再试。")
            cursor = conn.execute(
                """INSERT INTO reservations(product_id, buyer_id, status, created_at)
                   VALUES (?, ?, ?, ?)""",
                (product_id, buyer.id, ReservationStatus.PENDING, self._now()),
            )
            self.log(conn, buyer.id, "发起预约", "预约", cursor.lastrowid, "成功")

    def reservations_for(
        self, user: User, received: bool = False, status: str = "全部"
    ) -> list[sqlite3.Row]:
        join = "p.seller_id = ?" if received else "r.buyer_id = ?"
        status_clause = "" if status == "全部" else " AND r.status = ?"
        values: list[object] = [user.id]
        if status != "全部":
            values.append(status)
        with self.transaction() as conn:
            return conn.execute(
                f"""SELECT r.*, p.title, p.price, p.image_icon, p.delivery_method, p.status AS product_status,
                           buyer.nickname AS buyer_name, seller.nickname AS seller_name
                    FROM reservations r JOIN products p ON p.id = r.product_id
                    JOIN users buyer ON buyer.id = r.buyer_id
                    JOIN users seller ON seller.id = p.seller_id
                    WHERE {join}{status_clause} ORDER BY r.id DESC""",
                values,
            ).fetchall()

    def cancel_or_reject(self, user: User, reservation_id: int, reject: bool = False) -> None:
        with self.transaction() as conn:
            row = conn.execute(
                """SELECT r.*, p.seller_id, p.status AS product_status FROM reservations r
                   JOIN products p ON p.id = r.product_id WHERE r.id = ?""",
                (reservation_id,),
            ).fetchone()
            if row is None:
                raise BusinessError("预约不存在。")
            permitted = user.id == row["seller_id"] if reject else user.id == row["buyer_id"]
            if not permitted:
                raise BusinessError("无权处理该预约。")
            if row["seller_delivered_at"] or row["status"] not in (
                ReservationStatus.PENDING, ReservationStatus.CONFIRMED
            ):
                raise BusinessError("当前预约无法取消或拒绝。")
            target = ReservationStatus.REJECTED if reject else ReservationStatus.CANCELLED
            conn.execute("UPDATE reservations SET status = ? WHERE id = ?", (target, reservation_id))
            conn.execute(
                """UPDATE products SET status = ?, version = version + 1
                   WHERE id = ? AND status = ?""",
                (ProductStatus.ON_SALE, row["product_id"], ProductStatus.RESERVED),
            )
            action = "拒绝预约" if reject else "取消预约"
            self.log(conn, user.id, action, "预约", reservation_id, "成功")

    def confirm_reservation(self, seller: User, reservation_id: int) -> None:
        self._seller_reservation_action(seller, reservation_id, "confirm")

    def confirm_delivery(self, seller: User, reservation_id: int) -> None:
        self._seller_reservation_action(seller, reservation_id, "deliver")

    def _seller_reservation_action(self, seller: User, reservation_id: int, action: str) -> None:
        self._require_role(seller, Roles.SELLER)
        with self.transaction() as conn:
            row = conn.execute(
                """SELECT r.*, p.seller_id FROM reservations r JOIN products p ON p.id = r.product_id
                   WHERE r.id = ?""", (reservation_id,)
            ).fetchone()
            if row is None or row["seller_id"] != seller.id:
                raise BusinessError("无权处理该预约。")
            if action == "confirm":
                if row["status"] != ReservationStatus.PENDING:
                    raise BusinessError("仅待确认预约可被确认。")
                conn.execute(
                    "UPDATE reservations SET status = ? WHERE id = ?",
                    (ReservationStatus.CONFIRMED, reservation_id),
                )
                self.log(conn, seller.id, "确认预约", "预约", reservation_id, "成功")
            else:
                if row["status"] != ReservationStatus.CONFIRMED or row["seller_delivered_at"]:
                    raise BusinessError("请先确认预约，且不能重复确认交付。")
                conn.execute(
                    "UPDATE reservations SET seller_delivered_at = ? WHERE id = ?",
                    (self._now(), reservation_id),
                )
                self.log(conn, seller.id, "确认交付", "预约", reservation_id, "成功")

    def confirm_receipt(self, buyer: User, reservation_id: int) -> None:
        self._require_role(buyer, Roles.BUYER)
        with self.transaction() as conn:
            row = conn.execute(
                "SELECT * FROM reservations WHERE id = ?", (reservation_id,)
            ).fetchone()
            if row is None or row["buyer_id"] != buyer.id:
                raise BusinessError("无权确认该预约。")
            if row["status"] != ReservationStatus.CONFIRMED or not row["seller_delivered_at"]:
                raise BusinessError("请等待卖家确认交付后再确认收货。")
            conn.execute(
                """UPDATE reservations SET status = ?, buyer_received_at = ? WHERE id = ?""",
                (ReservationStatus.FINISHED, self._now(), reservation_id),
            )
            conn.execute(
                """UPDATE products SET status = ?, version = version + 1
                   WHERE id = ? AND status = ?""",
                (ProductStatus.SOLD, row["product_id"], ProductStatus.RESERVED),
            )
            self.log(conn, buyer.id, "确认收货", "预约", reservation_id, "成功")

    def toggle_favorite(self, buyer: User, product_id: int) -> bool:
        self._require_role(buyer, Roles.BUYER)
        with self.transaction() as conn:
            product = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
            if product is None or product["status"] in (
                ProductStatus.OFF_SHELF,
                ProductStatus.VIOLATION,
            ):
                raise BusinessError("该商品当前不可收藏。")
            if product["seller_id"] == buyer.id:
                raise BusinessError("不能收藏自己发布的商品。")
            row = conn.execute(
                "SELECT id FROM favorites WHERE buyer_id = ? AND product_id = ?",
                (buyer.id, product_id),
            ).fetchone()
            if row:
                conn.execute("DELETE FROM favorites WHERE id = ?", (row["id"],))
                self.log(conn, buyer.id, "取消收藏", "商品", product_id, "成功")
                return False
            conn.execute(
                "INSERT INTO favorites(buyer_id, product_id, created_at) VALUES (?, ?, ?)",
                (buyer.id, product_id, self._now()),
            )
            self.log(conn, buyer.id, "收藏商品", "商品", product_id, "成功")
            return True

    def favorites(self, buyer: User) -> list[sqlite3.Row]:
        self._require_role(buyer, Roles.BUYER)
        with self.transaction() as conn:
            return conn.execute(
                """SELECT p.*, u.nickname AS seller_name FROM favorites f
                   JOIN products p ON p.id = f.product_id JOIN users u ON u.id = p.seller_id
                   WHERE f.buyer_id = ? ORDER BY f.id DESC""", (buyer.id,)
            ).fetchall()

    def report(self, user: User, product_id: int, reason: str) -> None:
        if not reason.strip():
            raise BusinessError("请填写举报原因。")
        with self.transaction() as conn:
            product = conn.execute("SELECT seller_id, status FROM products WHERE id = ?", (product_id,)).fetchone()
            if product is None or product["status"] in (
                ProductStatus.OFF_SHELF,
                ProductStatus.VIOLATION,
            ):
                raise BusinessError("该商品当前不可举报。")
            existing = conn.execute(
                "SELECT 1 FROM reports WHERE reporter_id = ? AND product_id = ? AND status = '待处理'",
                (user.id, product_id),
            ).fetchone()
            if existing:
                raise BusinessError("你已提交过该商品的待处理举报。")
            cursor = conn.execute(
                """INSERT INTO reports(reporter_id, product_id, reason, created_at)
                   VALUES (?, ?, ?, ?)""", (user.id, product_id, reason.strip(), self._now())
            )
            self.log(conn, user.id, "举报商品", "举报", cursor.lastrowid, "成功")

    def reports(self, admin: User) -> list[sqlite3.Row]:
        self._require_role(admin, Roles.ADMIN)
        with self.transaction() as conn:
            return conn.execute(
                """SELECT r.*, p.title, reporter.nickname AS reporter_name FROM reports r
                   JOIN products p ON p.id = r.product_id
                   JOIN users reporter ON reporter.id = r.reporter_id
                   ORDER BY r.id DESC"""
            ).fetchall()

    def handle_report(self, admin: User, report_id: int, violation: bool, reason: str) -> None:
        self._require_role(admin, Roles.ADMIN)
        if not reason.strip():
            raise BusinessError("请填写处理说明。")
        with self.transaction() as conn:
            row = conn.execute("SELECT * FROM reports WHERE id = ?", (report_id,)).fetchone()
            if row is None or row["status"] != "待处理":
                raise BusinessError("该举报已被处理。")
            result = "违规确认" if violation else "已驳回"
            conn.execute(
                """UPDATE reports SET status = ?, handler_id = ?, result = ?, handled_at = ?
                   WHERE id = ?""", (result, admin.id, reason.strip(), self._now(), report_id)
            )
            if violation:
                conn.execute(
                    """UPDATE products SET status = ?, violation_reason = ?, version = version + 1
                       WHERE id = ?""", (ProductStatus.VIOLATION, reason.strip(), row["product_id"])
                )
            self.log(conn, admin.id, "处理举报", "举报", report_id, "成功", reason.strip())

    def statistics(self, admin: User) -> dict[str, int]:
        self._require_role(admin, Roles.ADMIN)
        with self.transaction() as conn:
            rows = conn.execute(
                "SELECT status, COUNT(*) AS amount FROM products GROUP BY status"
            ).fetchall()
            return {row["status"]: row["amount"] for row in rows}

    def logs(self, admin: User) -> list[sqlite3.Row]:
        self._require_role(admin, Roles.ADMIN)
        with self.transaction() as conn:
            return conn.execute(
                """SELECT l.*, COALESCE(u.nickname, '系统') AS operator_name
                   FROM operation_logs l LEFT JOIN users u ON u.id = l.operator_id
                   ORDER BY l.id DESC LIMIT 50"""
            ).fetchall()

    @staticmethod
    def _require_role(user: User, role: str) -> None:
        if user.role != role:
            raise BusinessError("当前账号没有此操作权限。")
