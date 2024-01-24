import wolframalpha

APP_ID = '3A3K4Y-PVYG57G8QE'

def solve(question):
    client = wolframalpha.Client(APP_ID)

    # Stores the response from wolfram alpha
    res = client.query(question)

    # Includes only text from the response
    answer = next(res.results).text

    return answer[7:]

def main() -> None:
    pass

if __name__ == '__main__':
    main()
    