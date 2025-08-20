from downloader import ydl


def main():
  ydl.download(['https://www.youtube.com/watch?v=y4FiCl-tUJc&list=LL&index=1'])

if __name__ == '__main__':
  # import asyncio
  # asyncio.run(main())
  main()