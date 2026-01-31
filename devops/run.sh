#!/bin/bash
trap state ERR EXIT

function state() {
  exit $?
}

function log() {
  echo "$(date): $1"
}

function compose() {
  docker compose "$@"
}

function build_containers() {
  log "Building containers"
  compose build mars-rover
}

function check_code() {
  log "Check for unused/dead code"
  compose run mars-rover vulture app/ test/ whitelist.py
}

function run_tests() {
  local test_path="$1"
  if [ -n "$test_path" ]; then
    log "Running tests for $test_path"
    pytest -s -vv --durations=50 "$test_path"
  else
    log "Running tests"
    pytest -s -vv --durations=50
  fi
}

function run_ci() {
  local test_path="$1"
  log "Running CI pipeline with docker compose"
  compose up  mars-rover -d 
  if [ -n "$test_path" ]; then
    compose exec -it mars-rover devops/run.sh test "$test_path"
  else
    compose exec -it mars-rover devops/run.sh test
  fi
}

function shutdown_containers() {
  log "Shutdown containers"
  docker network prune --force && compose down --remove-orphans --volumes
}

function show_help() {
  cat << EOF
CI Pipeline Script - Docker Compose Build & Test Automation

USAGE:
  ./devops/run.sh <command>

AVAILABLE COMMANDS:

  build      - Build Docker containers for the mars-rover service
             - Executes: docker compose build mars-rover
             - Use this when Dockerfile or dependencies have changed

  check      - Check for unused/dead code using Vulture
             - Executes: vulture app/ test/ whitelist.py
             - Identifies unreachable code and unused variables

  test       - Run all tests with pytest locally
             - Executes: pytest -s -vv --durations=50
             - Shows test output, verbose logging, and slowest tests

  ci         - Run tests inside docker container using compose
             - Executes: docker compose run mars-rover pytest -s -vv --durations=50
             - Tests run in isolated Docker environment with dependencies

  shutdown   - Clean up Docker resources
             - Prunes unused networks and removes containers/volumes
             - Use this to free up system resources

  all        - Run the complete CI pipeline (DEFAULT)
             - Runs in order: build → check → test → shutdown
             - This is the default if no command is specified

  help       - Display this help message

EXAMPLES:
  ./devops/run.sh                 # Run full pipeline (equivalent to 'all')
  ./devops/run.sh build           # Only build containers
  ./devops/run.sh test            # Only run tests locally
  ./devops/run.sh ci              # Run tests in docker container
  ./devops/run.sh check           # Only check for dead code
  ./devops/run.sh ci shutdown     # Not supported - use individual commands

EOF
}

# Main script with case statement
COMMAND="${1:-all}"

case "$COMMAND" in
  build)
    build_containers
    ;;
  check)
    check_code
    ;;
  test)
    run_tests "$2"
    ;;
  ci)
    run_ci "$2"
    ;;
  shutdown)
    shutdown_containers
    ;;
  all)
    build_containers
    check_code
    run_tests
    shutdown_containers
    ;;
  help)
    show_help
    ;;
  *)
    echo "Error: Unknown command '$COMMAND'"
    echo ""
    show_help
    exit 1
    ;;
esac
