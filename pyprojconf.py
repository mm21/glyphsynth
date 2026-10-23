from pyprojkit import (
    ProjectConfig,
    PythonVersions,
    RequiresPython,
    create_recommended_tools,
)

config = ProjectConfig(
    packages="glyphsynth",
    requires_python=RequiresPython((3, 12)),
    pinned_python=PythonVersions(3, (12, 14)),
    tools=create_recommended_tools(),
    typed=True,
)
