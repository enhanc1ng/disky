from diskyv2.utility import OP

import zlib
import json


class Listener:
    def __init__(self):
        return

    def callback(self):
        return "LISTENER NOT SET"

    def set_callback(self, function):
        self.callback = function

class Event:
    def __init__(self, data):
        self.parsed_data = json.loads(data)
        self.opcode = self.parsed_data.get("op")
        self.type = str(self.parsed_data.get("t"))
        self.data = self.parsed_data.get("d")
        self.sequence = self.parsed_data.get("s")

    #TYPES
    @property
    def READY(self):
        return "READY" in self.type

    @property
    def GUILD_CREATE(self):
        return "GUILD_CREATE" in self.type

    @property
    def GUILD_UPDATE(self):
        return "GUILD_UPDATE" in self.type

    @property
    def GUILD_DELETE(self):
        return "GUILD_DELETE" in self.type

    @property
    def GUILD_ROLE_CREATE(self):
        return "GUILD_ROLE_CREATE" in self.type

    @property
    def GUILD_ROLE_UPDATE(self):
        return "GUILD_ROLE_UPDATE" in self.type

    @property
    def GUILD_ROLE_DELETE(self):
        return "GUILD_ROLE_DELETE" in self.type

    @property
    def CHANNEL_CREATE(self):
        return "CHANNEL_CREATE" in self.type

    @property
    def CHANNEL_UPDATE(self):
        return "CHANNEL_UPDATE" in self.type

    @property
    def CHANNEL_DELETE(self):
        return "CHANNEL_DELETE" in self.type

    @property
    def CHANNEL_PINS_UPDATE(self):
        return "CHANNEL_PINS_UPDATE" in self.type

    @property
    def THREAD_CREATE(self):
        return "THREAD_CREATE" in self.type

    @property
    def THREAD_UPDATE(self):
        return "THREAD_UPDATE" in self.type

    @property
    def THREAD_DELETE(self):
        return "THREAD_DELETE" in self.type

    @property
    def THREAD_LIST_SYNC(self):
        return "THREAD_LIST_SYNC" in self.type

    @property
    def THREAD_MEMBER_UPDATE(self):
        return "THREAD_MEMBER_UPDATE" in self.type

    @property
    def THREAD_MEMBERS_UPDATE(self):
        return "THREAD_MEMBERS_UPDATE" in self.type

    @property
    def STAGE_INSTANCE_CREATE(self):
        return "STAGE_INSTANCE_CREATE" in self.type

    @property
    def STAGE_INSTANCE_UPDATE(self):
        return "STAGE_INSTANCE_UPDATE" in self.type

    @property
    def STAGE_INSTANCE_DELETE(self):
        return "STAGE_INSTANCE_DELETE" in self.type

    @property
    def GUILD_MEMBER_ADD(self):
        return "GUILD_MEMBER_ADD" in self.type

    @property
    def GUILD_MEMBER_UPDATE(self):
        return "GUILD_MEMBER_UPDATE" in self.type

    @property
    def GUILD_MEMBER_REMOVE(self):
        return "GUILD_MEMBER_REMOVE" in self.type

    @property
    def GUILD_AUDIT_LOG_ENTRY_CREATE(self):
        return "GUILD_AUDIT_LOG_ENTRY_CREATE" in self.type

    @property
    def GUILD_BAN_ADD(self):
        return "GUILD_BAN_ADD" in self.type

    @property
    def GUILD_BAN_REMOVE(self):
        return "GUILD_BAN_REMOVE" in self.type

    @property
    def GUILD_EMOJIS_UPDATE(self):
        return "GUILD_EMOJIS_UPDATE" in self.type

    @property
    def GUILD_STICKERS_UPDATE(self):
        return "GUILD_STICKERS_UPDATE" in self.type

    @property
    def GUILD_INTEGRATIONS_UPDATE(self):
        return "GUILD_INTEGRATIONS_UPDATE" in self.type

    @property
    def INTEGRATION_CREATE(self):
        return "INTEGRATION_CREATE" in self.type

    @property
    def INTEGRATION_UPDATE(self):
        return "INTEGRATION_UPDATE" in self.type

    @property
    def INTEGRATION_DELETE(self):
        return "INTEGRATION_DELETE" in self.type

    @property
    def WEBHOOKS_UPDATE(self):
        return "WEBHOOKS_UPDATE" in self.type

    @property
    def INVITE_CREATE(self):
        return "INVITE_CREATE" in self.type

    @property
    def INVITE_DELETE(self):
        return "INVITE_DELETE" in self.type

    @property
    def VOICE_STATE_UPDATE(self):
        return "VOICE_STATE_UPDATE" in self.type

    @property
    def PRESENCE_UPDATE(self):
        return "PRESENCE_UPDATE" in self.type

    @property
    def MESSAGE_CREATE(self):
        return "MESSAGE_CREATE" in self.type

    @property
    def MESSAGE_UPDATE(self):
        return "MESSAGE_UPDATE" in self.type

    @property
    def MESSAGE_DELETE(self):
        return "MESSAGE_DELETE" in self.type

    @property
    def MESSAGE_DELETE_BULK(self):
        return "MESSAGE_DELETE_BULK" in self.type

    @property
    def MESSAGE_REACTION_ADD(self):
        return "MESSAGE_REACTION_ADD" in self.type

    @property
    def MESSAGE_REACTION_REMOVE(self):
        return "MESSAGE_REACTION_REMOVE" in self.type

    @property
    def MESSAGE_REACTION_REMOVE_ALL(self):
        return "MESSAGE_REACTION_REMOVE_ALL" in self.type

    @property
    def MESSAGE_REACTION_REMOVE_EMOJI(self):
        return "MESSAGE_REACTION_REMOVE_EMOJI" in self.type

    @property
    def TYPING_START(self):
        return "TYPING_START" in self.type

    @property
    def GUILD_SCHEDULED_EVENT_CREATE(self):
        return "GUILD_SCHEDULED_EVENT_CREATE" in self.type

    @property
    def GUILD_SCHEDULED_EVENT_UPDATE(self):
        return "GUILD_SCHEDULED_EVENT_UPDATE" in self.type

    @property
    def GUILD_SCHEDULED_EVENT_DELETE(self):
        return "GUILD_SCHEDULED_EVENT_DELETE" in self.type

    @property
    def GUILD_SCHEDULED_EVENT_USER_ADD(self):
        return "GUILD_SCHEDULED_EVENT_USER_ADD" in self.type

    @property
    def GUILD_SCHEDULED_EVENT_USER_REMOVE(self):
        return "GUILD_SCHEDULED_EVENT_USER_REMOVE" in self.type

    @property
    def AUTO_MODERATION_RULE_CREATE(self):
        return "AUTO_MODERATION_RULE_CREATE" in self.type

    @property
    def AUTO_MODERATION_RULE_UPDATE(self):
        return "AUTO_MODERATION_RULE_UPDATE" in self.type

    @property
    def AUTO_MODERATION_RULE_DELETE(self):
        return "AUTO_MODERATION_RULE_DELETE" in self.type


    @property
    def AUTO_MODERATION_ACTION_EXECUTION(self):
        return "AUTO_MODERATION_ACTION_EXECUTION" in self.type

    @property
    def MESSAGE_POLL_VOTE_ADD(self):
        return "MESSAGE_POLL_VOTE_ADD" in self.type

    @property
    def MESSAGE_POLL_VOTE_REMOVE(self):
        return "MESSAGE_POLL_VOTE_REMOVE" in self.type


    #OPCODES
    @property
    def HEARTBEAT(self):
        return self.opcode is OP.Heartbeat

    @property
    def HEARTBEAT_DATA(self):
        return self.opcode is OP.Heartbeat_DATA

    @property
    def HEARTBEAT_ACK(self):
        return self.opcode is OP.Heartbeat_ACK

    @property
    def RECONNECT(self):
        return self.opcode is OP.Reconnect

    @property
    def INVALID_SESSION(self):
        return self.opcode is OP.Invalid_Session

class AvatarDecoration:
    def __init__(self, asset=None, sku_id=None):
        self.asset = asset
        self.sku_id = sku_id

class User:
    def __init__(self, verified, username, purchased_flags, pronouns, premium_type, premium,
                 phone, nsfw_allowed, mobile, mfa_enabled, id, global_name, flags, email,
                 discriminator, desktop, clan, bio, banner_color, banner, avatar_decoration_data,
                 avatar, accent_color, public_flags=None, premium_usage_flags=None):
        self.verified = verified
        self.username = username
        self.purchased_flags = purchased_flags
        self.premium_usage_flags = premium_usage_flags
        self.public_flags = public_flags
        self.pronouns = pronouns
        self.premium_type = premium_type
        self.premium = premium
        self.phone = phone
        self.nsfw_allowed = nsfw_allowed
        self.mobile = mobile
        self.mfa_enabled = mfa_enabled
        self.id = id
        self.global_name = global_name
        self.flags = flags
        self.email = email
        self.discriminator = discriminator
        self.desktop = desktop
        self.clan = clan
        self.bio = bio
        self.banner_color = banner_color
        self.banner = banner
        self.avatar_decoration = AvatarDecoration(**avatar_decoration_data) if avatar_decoration_data else None
        self.avatar = avatar
        self.accent_color = accent_color