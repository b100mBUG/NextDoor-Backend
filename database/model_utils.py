import enum


class UserRole(str, enum.Enum):
    TENANT = "tenant"
    LANDLORD = "landlord"
    AGENT = "agent"
    ADMIN = "admin"


class HouseType(str, enum.Enum):
    BEDSITTER = "bedsitter"
    ONE_BEDROOM = "1br"
    TWO_BEDROOM = "2br"
    THREE_BEDROOM = "3br"
    FOUR_BEDROOM = "4br"


class WaterSupply(str, enum.Enum):
    FULL_24_7 = "24_7"
    SCHEDULED = "scheduled"
    BOREHOLE = "borehole"
    NONE = "none"


class BathroomType(str, enum.Enum):
    PRIVATE = "private"
    SHARED = "shared"


class KitchenType(str, enum.Enum):
    PRIVATE = "private"
    SHARED = "shared"


class SecurityLevel(str, enum.Enum):
    NONE = "none"
    GATE = "gate"
    CARETAKER = "caretaker"
    CCTV = "cctv"
    FULL = "full"


class MediaType(str, enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
