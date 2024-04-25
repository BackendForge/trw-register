import requests

REGISTER_ENDPOINT = "https://api.princeofcrypto.com/v1/user/register?username={}"


def require_confirm_loop(message: str):
    while True:
        answer = input(f"{message} (Y/N): ").lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False


def require_answer_loop(message: str, default: str):
    while True:
        answer = input(f"{message}: [{default}] ")
        if answer == "":
            return default
        return answer


def main():
    while True:
        username = require_answer_loop("Enter your username", "Sun Tzu")
        if require_confirm_loop(f'Is "{username}" your username?'):
            break
    print(f"\nHello, {username}!")
    print("I will register you into OVERKILL platform.")
    print("Please wait for a moment...\n")
    try:
        res = requests.post(
            REGISTER_ENDPOINT.format(username),
            headers={"Content-Type": "application/json"},
        )
        res.raise_for_status()  # Check the response status code and raise an exception for non-200 status codes
    except requests.exceptions.RequestException as e:
        err_details = e.response.json()
        print(f'{err_details.get("result", "Unknown error occurred!")}')
        return
    user_data = res.get("result", "Unknown error occurred!")
    success_message = f"""You have been successfully registered!
    username: {user_data.get("user_id")}
    password: {user_data.get("password")}
    X_API_KEY: {user_data.get("x_api_key")}
    X_API_SECRET: {user_data.get("x_api_secret")}
    Please keep your password in a safe place! Password & X_API_SECRET are not recoverable.
    """
    print(success_message)


if __name__ == "__main__":
    main()
