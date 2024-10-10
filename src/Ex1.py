
class Song:

    def phrase1(self,a):
        return f"{a} kilomètre{'s'*(a>1)} à pied, ¸ca use, ¸ca use,"

    def phrase2(self,a):
        return f"{a} kilomètre{'s' * (a>1)} à pied, ca use les souliers."

    def sing(self,n):
        song = ''
        for I in range(1,n+1):
            song += f"{self.phrase1(I)}\n{self.phrase2(I)}\n\n"
        return song.strip()

if __name__ == "__main__":
    print(Song().sing(0))
    print("test")