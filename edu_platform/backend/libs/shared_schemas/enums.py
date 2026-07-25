import enum


class UserRole(str, enum.Enum):
    school_owner = "school_owner"      # Onlayn maktab egasiman
    expert_teacher = "expert_teacher"  # Individual ekspert/o'qituvchiman
    producer = "producer"              # Prodyuserman
    corporate_hr = "corporate_hr"      # Korporativ o'qitish
    student = "student"                # O'quvchi / Talaba
    other = "other"                    # Boshqa


class PaymentStatus(str, enum.Enum):
    pending = "pending"
    paid = "paid"
    failed = "failed"
    refunded = "refunded"


class EnrollmentStatus(str, enum.Enum):
    active = "active"
    completed = "completed"
    blocked = "blocked"


class VideoStatus(str, enum.Enum):
    uploading = "uploading"
    processing = "processing"
    ready = "ready"
    error = "error"


class CrmSyncStatus(str, enum.Enum):
    pending = "pending"
    synced = "synced"
    failed = "failed"
