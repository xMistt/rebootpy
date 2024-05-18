.. currentmodule:: rebootpy

API Reference
===============

The following section outlines the API of rebootpy's command extension module.

.. _ext_commands_api_bot:

Bot
----

.. attributetable:: rebootpy.ext.commands.Bot

.. autoclass:: rebootpy.ext.commands.Bot
    :members:
    :inherited-members:

.. _ext_commands_api_events:

Event Reference
-----------------

These events function similar to :ref:`the regular events <rebootpy-api-events>`, except they
are custom to the command extension module.

.. function:: event_command_error(ctx, error)

    An error handler that is called when an error is raised
    inside a command either through user input error, check
    failure, or an error in your own code.

    Command error handlers are raised in a specific order. Returning
    ``False`` in any of them will invoke the next handler in the chain. If
    there are no handlers left to call, then the error is printed to
    stderr (console).

    The order goes as follows:
    1. The local command error handler is called. (Handler specified by decorating a command error handler with :meth:`Command.error()`)
    2. The local cog command error handler is called.
    3. All :func:`.event_command_error()` handlers are called
    simultaneously. If any of them return False, then the error will
    be printed.

    :param ctx: The invocation context.
    :type ctx: :class:`.Context`
    :param error: The error that was raised.
    :type error: :class:`.CommandError` derived

.. function:: event_command(ctx)

    An event that is called when a command is found and is about to be invoked.

    This event is called regardless of whether the command itself succeeds via
    error or completes.

    :param ctx: The invocation context.
    :type ctx: :class:`.Context`

.. function:: event_command_completion(ctx)

    An event that is called when a command has completed its invocation.

    This event is called only if the command succeeded, i.e. all checks have
    passed and the user input it correctly.

    :param ctx: The invocation context.
    :type ctx: :class:`.Context`

.. _ext_commands_api_command:

Command
--------

command()
~~~~~~~~~

.. autofunction:: rebootpy.ext.commands.command

group()
~~~~~~~

.. autofunction:: rebootpy.ext.commands.group

Command
~~~~~~~

.. attributetable:: rebootpy.ext.commands.Command

.. autoclass:: rebootpy.ext.commands.Command
    :members:
    :special-members: __call__

Group
~~~~~

.. attributetable:: rebootpy.ext.commands.Group

.. autoclass:: rebootpy.ext.commands.Group
    :members:
    :inherited-members:

GroupMixin
~~~~~~~~~~

.. attributetable:: rebootpy.ext.commands.GroupMixin

.. autoclass:: rebootpy.ext.commands.GroupMixin
    :members:

.. _ext_commands_api_cogs:

Cogs
------

Cog
~~~

.. attributetable:: rebootpy.ext.commands.Cog

.. autoclass:: rebootpy.ext.commands.Cog
    :members:

CogMeta
~~~~~~~

.. attributetable:: rebootpy.ext.commands.CogMeta

.. autoclass:: rebootpy.ext.commands.CogMeta
    :members:

.. _ext_commands_api_formatters:

Help Commands
-----------------

HelpCommand
~~~~~~~~~~~

.. attributetable:: rebootpy.ext.commands.HelpCommand

.. autoclass:: rebootpy.ext.commands.HelpCommand
    :members:

FortniteHelpCommand
~~~~~~~~~~~~~~~~~~~

.. attributetable:: rebootpy.ext.commands.FortniteHelpCommand

.. autoclass:: rebootpy.ext.commands.FortniteHelpCommand
    :members:
    :exclude-members: send_bot_help, send_cog_help, send_group_help, send_command_help, prepare_help_command

Paginator
~~~~~~~~~

.. attributetable:: rebootpy.ext.commands.Paginator

.. autoclass:: rebootpy.ext.commands.Paginator
    :members:

Enums
------

.. class:: rebootpy.ext.commands.BucketType

    Specifies a type of bucket for, e.g. a cooldown.

    .. attribute:: default

        The default bucket operates on a global basis.
    .. attribute:: user

        The user bucket operates on a per-user basis.


.. _ext_commands_api_checks:

Checks
-------

.. autofunction:: rebootpy.ext.commands.check

.. autofunction:: rebootpy.ext.commands.check_any

.. autofunction:: rebootpy.ext.commands.cooldown

.. autofunction:: rebootpy.ext.commands.max_concurrency

.. autofunction:: rebootpy.ext.commands.before_invoke

.. autofunction:: rebootpy.ext.commands.after_invoke

.. autofunction:: rebootpy.ext.commands.party_only

.. autofunction:: rebootpy.ext.commands.dm_only

.. autofunction:: rebootpy.ext.commands.is_owner

.. _ext_commands_api_context:

Context
--------

.. attributetable:: rebootpy.ext.commands.Context

.. autoclass:: rebootpy.ext.commands.Context
    :members:
    :inherited-members:

.. _ext_commands_api_converters:

Converters
------------

.. autoclass:: rebootpy.ext.commands.Converter
    :members:

.. autoclass:: rebootpy.ext.commands.UserConverter
    :members:

.. autoclass:: rebootpy.ext.commands.FriendConverter
    :members:

.. autoclass:: rebootpy.ext.commands.PartyMemberConverter
    :members:

.. data:: ext.commands.Greedy

    A special converter that greedily consumes arguments until it can't.
    As a consequence of this behaviour, most input errors are silently discarded,
    since it is used as an indicator of when to stop parsing.

    When a parser error is met the greedy converter stops converting, undoes the
    internal string parsing routine, and continues parsing regularly.

    For example, in the following code:

    .. code-block:: python3

        @commands.command()
        async def test(ctx, numbers: Greedy[int], reason: str):
            await ctx.send("numbers: {}, reason: {}".format(numbers, reason))

    An invocation of ``[p]test 1 2 3 4 5 6 hello`` would pass ``numbers`` with
    ``[1, 2, 3, 4, 5, 6]`` and ``reason`` with ``hello``\.

    For more information, check :ref:`ext_commands_special_converters`.

.. _ext_commands_api_errors:

Exceptions
-----------

.. autoexception:: rebootpy.ext.commands.CommandError
    :members:

.. autoexception:: rebootpy.ext.commands.ConversionError
    :members:

.. autoexception:: rebootpy.ext.commands.MissingRequiredArgument
    :members:

.. autoexception:: rebootpy.ext.commands.ArgumentParsingError
    :members:

.. autoexception:: rebootpy.ext.commands.UnexpectedQuoteError
    :members:

.. autoexception:: rebootpy.ext.commands.InvalidEndOfQuotedStringError
    :members:

.. autoexception:: rebootpy.ext.commands.ExpectedClosingQuoteError
    :members:

.. autoexception:: rebootpy.ext.commands.BadArgument
    :members:

.. autoexception:: rebootpy.ext.commands.BadUnionArgument
    :members:

.. autoexception:: rebootpy.ext.commands.PrivateMessageOnly
    :members:

.. autoexception:: rebootpy.ext.commands.PartyMessageOnly
    :members:

.. autoexception:: rebootpy.ext.commands.CheckFailure
    :members:

.. autoexception:: rebootpy.ext.commands.CheckAnyFailure
    :members:

.. autoexception:: rebootpy.ext.commands.CommandNotFound
    :members:

.. autoexception:: rebootpy.ext.commands.DisabledCommand
    :members:

.. autoexception:: rebootpy.ext.commands.CommandInvokeError
    :members:

.. autoexception:: rebootpy.ext.commands.TooManyArguments
    :members:

.. autoexception:: rebootpy.ext.commands.UserInputError
    :members:

.. autoexception:: rebootpy.ext.commands.CommandOnCooldown
    :members:

.. autoexception:: rebootpy.ext.commands.MaxConcurrencyReached
    :members:

.. autoexception:: rebootpy.ext.commands.NotOwner
    :members:

.. autoexception:: rebootpy.ext.commands.ExtensionError
    :members:

.. autoexception:: rebootpy.ext.commands.ExtensionAlreadyLoaded
    :members:

.. autoexception:: rebootpy.ext.commands.ExtensionNotLoaded
    :members:

.. autoexception:: rebootpy.ext.commands.ExtensionMissingEntryPoint
    :members:

.. autoexception:: rebootpy.ext.commands.ExtensionFailed
    :members:

.. autoexception:: rebootpy.ext.commands.ExtensionNotFound
    :members:
