import click
import os
import json

try:
    from compliance_suite.test_runner import TestRunner
    from compliance_suite.report_server import start_mock_server
except:
    from test_runner import TestRunner
    from report_server import start_mock_server



@click.group()
def main():
    pass


@main.command(help='run compliance utility report using base urls')
@click.option('--server', '-s', multiple=True, help='base_url')
@click.option('--verbose', '-v', is_flag=True, help='to view the description and failure stack')
@click.option('--veryverbose', '-vv', is_flag=True, help='to view the description and failure stack')
# @click.option('--html', '-ht', default=None, help='generate html file')
# @click.option('--json', '-js', default=None, help='generate json file')
@click.option('--only_failures', '-of', default=None, help='show only failed cases in terminal report')
def report(server, veryverbose, verbose, only_failures):
    '''
    CLI command report to execute the report session and generate report on
    terminal, html file and json file if provided by the user

    Required arguments:
        server - Atleast one server is required. Multiple can be provided

    Optional arguments:
        --html - html file name for compliance matrix generation on html
        --json - json file name for machine readability

    Optional flags:
        -v - verbose for descriptive report on terminal
        --vv - veryverbose for even more description on terminal
        --of - only failure cases in the report on terminal
    '''
    final_json = []
    if verbose is True and veryverbose is True:
        raise Exception('Only one of -v and -vv can be used')
    if len(server) == 0:
        raise Exception('No server url provided. Provide atleast one')
    for s in server:
        tr = TestRunner(s)
        tr.run_tests()
        final_json.append(tr.generate_final_json())

    WEB_DIR = os.path.join(os.path.dirname(__file__), 'web')

    with open(os.path.join(WEB_DIR, 'temp_result' + '.json'), 'w+') as outfile:
        json.dump(final_json, outfile)

    start_mock_server()


if __name__ == "__main__":
    main()
