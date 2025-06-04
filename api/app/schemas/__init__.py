from pydantic import BaseModel, EmailStr
from typing import Optional

# ------------------------------
# 共通フィールドをまとめた基底クラス
# ------------------------------
class CandidateBase(BaseModel):
    full_name: str
    email: EmailStr                # <--- メール形式を自動バリデーション

# ------------------------------
# 「作成（POST）」で使う入力モデル
# ------------------------------
class CandidateCreate(CandidateBase):
    """受信専用：新しい候補者を登録するときのペイロード"""
    pass                            # 今は基底クラスと同じだが拡張しやすい

# ------------------------------
# 「更新（PUT / PATCH）」で使う入力モデル
# ------------------------------
class CandidateUpdate(BaseModel):
    """受信専用：特定フィールドだけ部分更新できるよう Optional に"""
    full_name: Optional[str] = None
    email:    Optional[EmailStr] = None

# ------------------------------
# 「レスポンス」で返すモデル
# ------------------------------
class CandidateOut(CandidateBase):
    id: int                         # DB が付与した主キーを含める

    class Config:
        orm_mode = True             # SQLAlchemy Row → Pydantic 変換を許可