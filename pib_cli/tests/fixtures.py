"""Test Fixtures"""

from unittest import TestCase
from unittest.mock import patch

from click.testing import CliRunner
from pib_cli.cli import cli


class CLITestHarness(TestCase):
  __test__ = False
  invocation_command = None
  internal_commands = [None]
  overload = None

  def setUp(self,):
    self.runner = CliRunner()
    self.invocation_command = self.__class__.invocation_command
    self.internal_command = self.__class__.internal_commands
    self.overload = self.__class__.overload

  @patch("pib_cli.cli.execute")
  @patch("pib_cli.support.paths.PathManager.is_container")
  def test_command_invocation_no_overload(self, mock_container, mock_execute):
    if self.overload is None:
      mock_container.return_value = True
      self.runner.invoke(cli, self.invocation_command)
      mock_execute.assert_called_once_with(self.internal_commands)

  @patch("pib_cli.cli.execute")
  @patch("pib_cli.support.paths.PathManager.is_container")
  def test_command_invocation_with_overload(self, mock_container, mock_execute):
    if self.overload is not None:
      mock_container.return_value = True
      self.runner.invoke(cli, self.invocation_command + list(self.overload))
      mock_execute.assert_called_once_with(
          self.internal_commands,
          overload=self.overload,
      )
