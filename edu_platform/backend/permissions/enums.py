import enum

class Permission(str, enum.Enum):

    VIEW_DASHBOARD = "view_dashboard"

    VIEW_COURSES = "view_courses"

    MANAGE_COURSES = "manage_courses"

    SUBMIT_HOMEWORK = "submit_homework"

    GRADE_HOMEWORKS = "grade_homeworks"

    VIEW_USERS = "view_users"

    MANAGE_USERS = "manage_users"

    VIEW_FINANCE = "view_finance"

    MANAGE_REFUNDS = "manage_refunds"

    MANAGE_PRODUCTS = "manage_products"

    MODERATE_COMMENTS = "moderate_comments"

    MANAGE_SETTINGS = "manage_settings"

class Role(str, enum.Enum):

    STUDENT = "student"

    CURATOR = "curator"

    MANAGER = "manager"

    ACCOUNTANT = "accountant"

    TEACHER = "teacher"

    ADMIN = "admin"

ROLE_PERMISSIONS = {

    Role.STUDENT: [

        Permission.VIEW_DASHBOARD,

        Permission.VIEW_COURSES,

        Permission.SUBMIT_HOMEWORK

    ],

    Role.CURATOR: [

        Permission.VIEW_DASHBOARD,

        Permission.VIEW_COURSES,

        Permission.GRADE_HOMEWORKS,

        Permission.VIEW_USERS,

        Permission.MODERATE_COMMENTS

    ],

    Role.TEACHER: [

        Permission.VIEW_DASHBOARD,

        Permission.VIEW_COURSES,

        Permission.MANAGE_COURSES,

        Permission.GRADE_HOMEWORKS,

        Permission.VIEW_USERS

    ],

    Role.MANAGER: [

        Permission.VIEW_DASHBOARD,

        Permission.VIEW_FINANCE,

        Permission.MANAGE_REFUNDS,

        Permission.MANAGE_PRODUCTS,

        Permission.VIEW_USERS

    ],

    Role.ACCOUNTANT: [

        Permission.VIEW_DASHBOARD,

        Permission.VIEW_FINANCE,

        Permission.MANAGE_REFUNDS,

        Permission.VIEW_USERS

    ],

    Role.ADMIN: [

        p for p in Permission

    ]

}

