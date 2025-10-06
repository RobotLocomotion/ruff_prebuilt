#!/bin/bash
# SPDX-License-Identifier: MIT

# When building with --config=release (see our .bazelrc), we want the files
# in the archive to be dated as of the most recent git commit, not 1970.
BUILD_TIMESTAMP=$(git log -1 --format="%ct")
echo "BUILD_TIMESTAMP ${BUILD_TIMESTAMP}"
