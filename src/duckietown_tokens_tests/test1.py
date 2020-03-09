import json
import os

from ecdsa import BadSignatureError

from duckietown_tokens import (
    create_signed_token,
    verify_token,
    DuckietownToken,
    get_id_from_token,
    InvalidToken,
)
from duckietown_tokens.duckietown_tokens import private

SAMPLE_TOKEN = (
    "dt1-9Hfd69b5ythetkCiNG12pKDrL987sLJT6KejWP2Eo5QQ"
    "-43dzqWFnWd8KBa1yev1g3UKnzVxZkkTbfWWn6of92V5Bf8qGV24rZHe6r7sueJNtWF"
)
SAMPLE_TOKEN_UID = -1
SAMPLE_TOKEN_EXP = "2018-10-20"


def tests_private():
    payload: str = json.dumps({"uid": SAMPLE_TOKEN_UID, "exp": SAMPLE_TOKEN_EXP})
    # generate a token
    token = create_signed_token(payload.encode())
    s = token.as_string()
    print(s)
    assert s == SAMPLE_TOKEN, (s, SAMPLE_TOKEN)
    token2 = token.from_string(s)

    assert verify_token(token2)


def test1():
    token = DuckietownToken.from_string(SAMPLE_TOKEN)
    assert verify_token(token)
    data = json.loads(token.payload)
    print(data)
    assert data["uid"] == SAMPLE_TOKEN_UID
    assert data["exp"] == SAMPLE_TOKEN_EXP

    seq = SAMPLE_TOKEN[6:8]
    msg_bad = SAMPLE_TOKEN.replace(seq, "XY")
    token = DuckietownToken.from_string(msg_bad)
    try:
        verify_token(token)
    except BadSignatureError:
        pass
    else:
        raise Exception(token)

    assert SAMPLE_TOKEN_UID == get_id_from_token(SAMPLE_TOKEN)

    try:
        get_id_from_token(msg_bad)
    except InvalidToken:
        pass
    else:
        raise Exception()


if __name__ == "__main__":
    if os.path.exists(private):
        tests_private()
    test1()
