"""
Created on Fri Oct 13 19:19:50 2023
@author: r.osipovskiy
"""
import os
import boto3
import json
import click


def apply2policy(policy : dict, bucket: str, prefix : str | None) -> dict:
    new = policy.copy()
    new["Statement"][0]["Resource"].append(f"arn:aws:s3:::{bucket}")
    new["Statement"][0]["Condition"]["StringLike"]["s3:prefix"] = [prefix]
    new["Statement"][1]["Resource"].append(f"arn:aws:s3:::{bucket}/{prefix}")
    return new


@click.command("minio token", no_args_is_help=True)
@click.option('-e', '--endpoint',  help='number of greetings')
@click.option('-ak', '--accesskey', help='number of greetings')
@click.option('-sk', '--secretkey', help='number of greetings')
@click.option('-b', '--bucket',    help='number of greetings')
@click.option('--prefix',  help='number of greetings')
@click.option('-l', '--lifetime',  help='number of greetings')
@click.option('-p', '--policy', default="R", help='number of greetings')
@click.option('--region', default='me-south-1', help='number of greetings')
@click.option('--output', default='stdout',  help='number of greetings')
def generate(endpoint: str,
         accesskey: str,
         secretkey,
         bucket,
         prefix,
         lifetime,
         policy : str,
         region : str,
         output : str
        ):
    """

    """
    if policy not in ["R", "W", "RW"]:
        raise Exception()

    if output not in ['stdout', 'json']:
        pass


    policy_files = os.listdir('./policies')
    target_policy = list(filter( lambda x : x.split(".json")[0].endswith(policy), policy_files))

    if not len(target_policy):
        raise Exception('There is no target policy')

    # loading template
    template_policy = json.load(os.path.join('./policies', policy_files[0]))
    # aplying values
    valid_policy = json.dumps(apply2policy(template_policy, bucket, prefix))

    client = boto3.client('sts',
                          endpoint_url = endpoint,
                          aws_access_key_id = accesskey,
                          aws_secret_access_key= secretkey,
                          region_name = region
                          )


    response = client.assume_role(
        RoleArn='arn:x:ignored:by:minio:',
        RoleSessionName='ignored-by-minio',
        Policy=valid_policy,
        DurationSeconds=lifetime,
    )
    if response.status_code != 200:
        pass
        # json.loads( reesponc
        print(f'{response.status_code}  {response.detail}')
        raise Exception

    if output == 'stdout':
        creds = response["Credentials"]
        # print json
        print(f'Key_id={creds["AccessKeyId"]}')
        print(f'Secret_key={creds["SecretAccessKey"]}')
        print(f'Token={creds["SessionToken"]}')
    else:
        # dump json-file
        with open('resp.json', 'w') as f:
            f.write(json.dumps(creds))


    if __name__ == '__main__':
        generate()
