

class FizzBuzz:


    def fibu(self,a):
        return f"{'Fizz'*(a%3==0)}{'Buzz'*(a%5==0)}"

    def loop(self,n):
        results = ""
        for I in range(1,n+1):
            r = f"{self.fibu(I)}"
            results += f"{f'{I}'*(r == "")}{r}\n"
        return results.strip()

if __name__ == "__main__":
    print(5%3)
    print(FizzBuzz().loop(15))