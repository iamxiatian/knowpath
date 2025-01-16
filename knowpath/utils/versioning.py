"""
Author: XiaTian xiat@ruc.edu.cn
Date: 2025-01-16 14:30:06
LastEditors: XiaTian xiat@ruc.edu.cn
LastEditTime: 2025-01-16 14:30:06
FilePath: /knowpath/knowpath/utils/versioning.py
Description:  获取版本信息，代码来自：https://github.com/OptimalScale/LMFlow/blob/main/src/lmflow/utils/versioning.py
"""

import importlib
import logging
import sys
from typing import List, Tuple, Union

logger = logging.getLogger(__name__)


def get_python_version() -> sys._version_info:
    return sys.version_info


def _is_package_available(package_name: str, skippable: bool = False):
    assert isinstance(package_name, str), (
        f"Invalid type of package_name: {type(package_name)}"
    )
    try:
        importlib.import_module(package_name)
        return True
    except Exception as e:
        if e.__class__ == ModuleNotFoundError:  # noqa: E721
            return False
        else:
            if skippable:
                logger.warning(
                    f"An error occurred when importing {package_name}:\n{e}\n{package_name} is disabled."
                )
                return False
            else:
                raise e


def is_packages_available(
    packages: Union[List[str], List[Tuple[str, bool]]],
) -> bool:
    if isinstance(packages[0], str):
        return all([_is_package_available(package) for package in packages])
    elif isinstance(packages[0], tuple):
        return all(
            [
                _is_package_available(package, skippable)
                for package, skippable in packages
            ]
        )
    else:
        raise ValueError(f"Invalid type of packages: {type(packages[0])}")
