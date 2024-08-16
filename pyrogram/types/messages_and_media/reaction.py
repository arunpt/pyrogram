#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Optional

import pyrogram
from pyrogram import raw
from ..object import Object


class Reaction(Object):
    """Contains information about a reaction.

    Parameters:
        emoji (``str``, *optional*):
            Reaction emoji.

        custom_emoji_id (``int``, *optional*):
            Custom emoji id.

        count (``int``, *optional*):
            Reaction count.

        chosen_order (``int``, *optional*):
            Chosen reaction order.
            Available for chosen reactions.

        is_paid (``bool``, *optional*):
            True, if this is a paid reaction.

    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        type: "types.ReactionType" = None,
        count: Optional[int] = None,
        chosen_order: Optional[int] = None,
        is_paid: Optional[bool] = None
    ):
        super().__init__(client)

        self.type = type
        self.count = count
        self.chosen_order = chosen_order

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        reaction: "raw.base.Reaction"
    ) -> "Reaction":
        if isinstance(reaction, raw.types.ReactionEmoji):
            return Reaction(
                client=client,
                type=ReactionEmoji(
                    emoji=reaction.emoticon
                )
            )

        if isinstance(reaction, raw.types.ReactionCustomEmoji):
            return Reaction(
                client=client,
                type=ReactionTypeCustomEmoji(
                    custom_emoji_id=reaction.document_id
                )
            )

        if isinstance(reaction, raw.types.ReactionPaid):
            return Reaction(
                client=client,
                type=ReactionTypePaid()
            )

    @staticmethod
    def _parse_count(
        client: "pyrogram.Client",
        reaction_count: "raw.base.ReactionCount"
    ) -> "Reaction":
        reaction = Reaction._parse(client, reaction_count.reaction)
        reaction.count = reaction_count.count
        reaction.chosen_order = reaction_count.chosen_order

        return reaction


class ReactionType(Object):
    """This object describes the type of a reaction. Currently, it can be one of

    - :obj:`~pyrogram.types.ReactionTypeEmoji`
    - :obj:`~pyrogram.types.ReactionTypeCustomEmoji`
    - :obj:`~pyrogram.types.ReactionTypePaid`

    """

    def __init__(
        self,
        *,
        type: str = None,
        emoji: str = None,
        custom_emoji_id: str = None
    ):
        super().__init__()
        self.type = type
        self.emoji = emoji
        self.custom_emoji_id = custom_emoji_id

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        update: "raw.types.Reaction",
    ) -> Optional["ReactionType"]:
        if isinstance(update, raw.types.ReactionEmpty):
            return None
        elif isinstance(update, raw.types.ReactionEmoji):
            return ReactionTypeEmoji(
                emoji=update.emoticon
            )
        elif isinstance(update, raw.types.ReactionCustomEmoji):
            return ReactionTypeCustomEmoji(
                custom_emoji_id=update.document_id
            )
        elif isinstance(update, raw.types.ReactionPaid):
            return ReactionTypePaid()

    def write(self, client: "pyrogram.Client"):
        raise NotImplementedError


class ReactionTypeEmoji(ReactionType):
    """The reaction is based on an emoji.

    Parameters:
        emoji (``str``, *optional*):
            Reaction emoji.
    """

    def __init__(
        self,
        *,
        emoji: str = None
    ):
        super().__init__(
            type="emoji",
            emoji=emoji
        )

    def write(self, client: "pyrogram.Client") -> "raw.base.Reaction":
        return raw.types.ReactionEmoji(
            emoticon=self.emoji
        )
        

class ReactionTypeCustomEmoji(ReactionType):
    """The reaction is based on a custom emoji.

    Parameters:
        custom_emoji_id (``str``, *optional*):
            Custom emoji id.
    """

    def __init__(
        self,
        *,
        custom_emoji_id: str = None
    ):
        super().__init__(
            type="custom_emoji",
            custom_emoji_id=custom_emoji_id
        )
    
    def write(self, client: "pyrogram.Client") -> "raw.base.Reaction":
        return raw.types.ReactionCustomEmoji(
            document_id=self.custom_emoji_id
        )


class ReactionTypePaid(ReactionType):
    """The paid reaction in a channel chat."""

    def __init__(self):
        super().__init__(
            type="paid"
        )
    
    def write(self, client: "pyrogram.Client") -> "raw.base.Reaction":
        return raw.types.ReactionPaid()


class ReactionCount(Object):
    """Represents a reaction added to a message along with the number of times it was added.

    Parameters:
        type (:obj:`~pyrogram.types.ReactionType`):
            Type of the reaction

        total_count (``int``):
            Reaction count.

        chosen_order (``int``):
            Chosen reaction order.
            Available for chosen reactions.
    """

    def __init__(
        self,
        *,
        type: ReactionType,
        total_count: int,
        chosen_order: int
    ):
        super().__init__()
        self.type = type
        self.total_count = total_count
        self.chosen_order = chosen_order

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        update: "raw.types.ReactionCount",
    ) -> Optional["ReactionCount"]:
        return ReactionCount(
            type=ReactionType._parse(
                client,
                update.reaction
            ),
            total_count=update.count,
            chosen_order=update.chosen_order
        )
