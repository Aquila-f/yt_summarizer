import argparse

import httpx

api_url = "http://127.0.0.1:8000/smr"


def arg_parser():
    parser = argparse.ArgumentParser(
        description="Send a POST request to FastAPI server."
    )
    parser.add_argument(
        "-i",
        "--inp_str",
        type=str,
        help="The URL of the YouTube video to summarize.",
        required=True,
    )
    return parser.parse_args()


def send_post_request(inp_str):
    try:
        response = httpx.post(api_url, json={"url": inp_str})

        if response.status_code == 200:
            print(f"Response received: {response.json()}")
        else:
            print(f"Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    args = arg_parser()

    send_post_request(args.inp_str)
