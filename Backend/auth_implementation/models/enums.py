from enum import Enum


class ProjectRole(str, Enum):
    """Project membership roles."""
    OWNER = "owner"
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


class AuditAction(str, Enum):
    """Audit log actions."""
    # Project actions
    PROJECT_CREATED = "project_created"
    PROJECT_UPDATED = "project_updated"
    PROJECT_DELETED = "project_deleted"
    PROJECT_SHARED = "project_shared"
    PROJECT_UNSHARED = "project_unshared"

    # User actions
    USER_REGISTERED = "user_registered"
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    PASSWORD_CHANGED = "password_changed"

    # Member actions
    MEMBER_ADDED = "member_added"
    MEMBER_REMOVED = "member_removed"
    MEMBER_ROLE_CHANGED = "member_role_changed"


class Permission(str, Enum):
    """System permissions."""
    # Project permissions
    PROJECT_CREATE = "project:create"
    PROJECT_READ = "project:read"
    PROJECT_UPDATE = "project:update"
    PROJECT_DELETE = "project:delete"
    PROJECT_SHARE = "project:share"

    # Member permissions
    MEMBER_INVITE = "member:invite"
    MEMBER_REMOVE = "member:remove"
    MEMBER_ROLE_CHANGE = "member:role_change"