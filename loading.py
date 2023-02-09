def progress_bar(progress, total):
    percent = 100 * (progress / float(total))
    bar = '█' * int(precent) + '-' * (100 - int(percent))
    print(f"\r|{bar}| {percent:.2f}%", end="\r")

    