from typing import Any, Callable, Optional
from .utils import copy_doc

__all__ = ("Permissions", "UserFlags")


class BaseFlags:
    value: int

    def __init__(self, value: int) -> None:
        self.value: int = value

    def __repr__(self):
        return f"<{self.__class__.__name__} value={self.value}>"

    def _has_flag(self, other: int) -> bool:
        return (self.value & other) == other


class flag:
    def __init__(self, f: Callable[[Any], int]) -> None:
        self.flag: int = f(None)
        self.__doc__: Optional[str] = f.__doc__

    def __get__(self, instance: BaseFlags, owner: Any):
        if instance is None:
            return None
        return instance._has_flag(self.flag)

    def __repr__(self):
        return "<flag flag={.flag!r}>".format(self)


flag_alias = flag


class Permissions(BaseFlags):
    __slots__ = ()

    @flag
    def create_instant_invite(self):
        """:class:`bool`: Returns ``True`` if the user can create instant invites."""
        return 1 << 0

    @flag
    def kick_members(self):
        """:class:`bool`: Returns ``True`` if the user can kick users from the guild."""
        return 1 << 1

    @flag
    def ban_members(self):
        """:class:`bool`: Returns ``True`` if a user can ban users from the guild."""
        return 1 << 2

    @flag
    def administrator(self):
        """:class:`bool`: Returns ``True`` if a user is an administrator. This role overrides all other permissions.
        This also bypasses all channel-specific overrides.
        """
        return 1 << 3

    @flag
    def manage_channels(self):
        """:class:`bool`: Returns ``True`` if a user can edit, delete, or create channels in the guild.
        This also corresponds to the "Manage Channel" channel-specific override."""
        return 1 << 4

    @flag
    def manage_guild(self):
        """:class:`bool`: Returns ``True`` if a user can edit guild properties."""
        return 1 << 5

    @flag
    def add_reactions(self):
        """:class:`bool`: Returns ``True`` if a user can add reactions to messages."""
        return 1 << 6

    @flag
    def view_audit_log(self):
        """:class:`bool`: Returns ``True`` if a user can view the guild's audit log."""
        return 1 << 7

    @flag
    def priority_speaker(self):
        """:class:`bool`: Returns ``True`` if a user can be more easily heard while talking."""
        return 1 << 8

    @flag
    def stream(self):
        """:class:`bool`: Returns ``True`` if a user can stream in a voice channel."""
        return 1 << 9

    @flag
    def read_messages(self):
        """:class:`bool`: Returns ``True`` if a user can read messages from all or specific text channels."""
        return 1 << 10

    @flag
    def send_messages(self):
        """:class:`bool`: Returns ``True`` if a user can send messages from all or specific text channels."""
        return 1 << 11

    @flag
    def send_tts_messages(self):
        """:class:`bool`: Returns ``True`` if a user can send TTS messages from all or specific text channels."""
        return 1 << 12

    @flag
    def manage_messages(self):
        """:class:`bool`: Returns ``True`` if a user can delete or pin messages in a text channel.
        .. note::
            Note that there are currently no ways to edit other people's messages.
        """
        return 1 << 13

    @flag
    def embed_links(self):
        """:class:`bool`: Returns ``True`` if a user's messages will automatically be embedded by Discord."""
        return 1 << 14

    @flag
    def attach_files(self):
        """:class:`bool`: Returns ``True`` if a user can send files in their messages."""
        return 1 << 15

    @flag
    def read_message_history(self):
        """:class:`bool`: Returns ``True`` if a user can read a text channel's previous messages."""
        return 1 << 16

    @flag
    def mention_everyone(self):
        """:class:`bool`: Returns ``True`` if a user's @everyone or @here will mention everyone in the text channel."""
        return 1 << 17

    @flag
    def external_emojis(self):
        """:class:`bool`: Returns ``True`` if a user can use emojis from other guilds."""
        return 1 << 18

    @flag
    def view_guild_insights(self):
        """:class:`bool`: Returns ``True`` if a user can view the guild's insights.
        .. versionadded:: 1.3
        """
        return 1 << 19

    @flag
    def connect(self):
        """:class:`bool`: Returns ``True`` if a user can connect to a voice channel."""
        return 1 << 20

    @flag
    def speak(self):
        """:class:`bool`: Returns ``True`` if a user can speak in a voice channel."""
        return 1 << 21

    @flag
    def mute_members(self):
        """:class:`bool`: Returns ``True`` if a user can mute other users."""
        return 1 << 22

    @flag
    def deafen_members(self):
        """:class:`bool`: Returns ``True`` if a user can deafen other users."""
        return 1 << 23

    @flag
    def move_members(self):
        """:class:`bool`: Returns ``True`` if a user can move users between other voice channels."""
        return 1 << 24

    @flag
    def use_voice_activation(self):
        """:class:`bool`: Returns ``True`` if a user can use voice activation in voice channels."""
        return 1 << 25

    @flag
    def change_nickname(self):
        """:class:`bool`: Returns ``True`` if a user can change their nickname in the guild."""
        return 1 << 26

    @flag
    def manage_nicknames(self):
        """:class:`bool`: Returns ``True`` if a user can change other user's nickname in the guild."""
        return 1 << 27

    @flag
    def manage_roles(self):
        """:class:`bool`: Returns ``True`` if a user can create or edit roles less than their role's position.
        This also corresponds to the "Manage Permissions" channel-specific override.
        """
        return 1 << 28

    @flag
    def manage_webhooks(self):
        """:class:`bool`: Returns ``True`` if a user can create, edit, or delete webhooks."""
        return 1 << 29

    @flag
    def manage_emojis(self):
        """:class:`bool`: Returns ``True`` if a user can create, edit, or delete emojis."""
        return 1 << 30

    @flag
    def use_slash_commands(self):
        """:class:`bool`: Returns ``True`` if a user can use slash commands."""
        return 1 << 31

    @flag
    def request_to_speak(self):
        """:class:`bool`: Returns ``True`` if a user can request to speak in a stage channel."""
        return 1 << 32


class UserFlags(BaseFlags):
    __slots__ = ()

    @flag
    def staff(self):
        """:class:`bool`: Returns ``True`` if the user is a Discord Employee."""
        return 1 << 0

    @flag
    def partner(self):
        """:class:`bool`: Returns ``True`` if the user is a Discord Partner."""
        return 1 << 1

    @flag
    def hypesquad(self):
        """:class:`bool`: Returns ``True`` if the user is a HypeSquad Events member."""
        return 1 << 2

    @flag
    def bug_hunter_level_1(self):
        """:class:`bool`: Returns ``True`` if the user is a bug hunter level 1."""
        return 1 << 3

    @flag_alias
    @copy_doc(bug_hunter_level_1)
    def bug_hunter(self):
        return 1 << 3

    @flag
    def hypesquad_online_house_1(self):
        """:class:`bool`: Returns ``True`` if the user is a HypeSquad Bravery member."""
        return 1 << 6

    @flag_alias
    @copy_doc(hypesquad_online_house_1)
    def hypesquad_bravery(self):
        return 1 << 6

    @flag
    def hypesquad_online_house_2(self):
        """:class:`bool`: Returns ``True`` if the user is a HypeSquad Brilliance member."""
        return 1 << 7

    @flag_alias
    @copy_doc(hypesquad_online_house_2)
    def hypesquad_brilliance(self):
        return 1 << 7

    @flag
    def hypesquad_online_house_3(self):
        """:class:`bool`: Returns ``True`` if the user is a HypeSquad Balance member."""
        return 1 << 8

    @flag_alias
    @copy_doc(hypesquad_online_house_3)
    def hypesquad_balance(self):
        return 1 << 8

    @flag
    def early_supporter(self):
        """:class:`bool`: Returns ``True`` if the user is an Early Supporter."""
        return 1 << 9

    @flag
    def team_pseudo_user(self):
        """:class:`bool`: Returns ``True`` if the user is a Team User."""
        return 1 << 10

    @flag_alias
    @copy_doc(team_pseudo_user)
    def team_user(self):
        return 1 << 10

    @flag
    def system(self):
        """:class:`bool`: Returns ``True`` if the user is a system user (i.e. represents Discord officially)."""
        return 1 << 12

    @flag
    def bug_hunter_level_2(self):
        """:class:`bool`: Returns ``True`` if the user is a Bug Hunter Level 2"""
        return 1 << 14

    @flag
    def verified_bot(self):
        """:class:`bool`: Returns ``True`` if the user is a Verified Bot."""
        return 1 << 16

    @flag
    def verified_developer(self):
        """:class:`bool`: Returns ``True`` if the user is an Early Verified Bot Developer."""
        return 1 << 17

    @flag
    def certified_moderator(self):
        """:class:`bool`: Returns ``True`` if the user is a Discord Certified Moderator."""
        return 1 << 18

    @flag
    def bot_http_interactions(self):
        """:class:`bool`: Returns ``True`` if the user is a bot that only uses HTTP interactions
        and is shown in the online member list."""
        return 1 << 19

    @flag
    def spammer(self):
        """:class:`bool`: Returns ``True`` if the user is flagged as a spammer by Discord."""
        return 1 << 20