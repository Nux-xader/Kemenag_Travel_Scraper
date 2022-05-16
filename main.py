import requests, pandas, json, sys, os
from bs4 import BeautifulSoup


log_file = "log.txt"
req_session = requests.Session()
timeout = 5
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
}


def write_log(e):
    open(log_file, "a").write(str(e)+" File : "+str(__file__)+" Line : "+str(e.__traceback__.tb_lineno)+"\n")

def network_err():
    input(" [!] please check your internet connection\n [Press Enter to continue]")
    sys.exit()


try:
    data = str(req_session.get("https://umrahcerdas.kemenag.go.id/home/travel", headers=headers, timeout=timeout).text)
except Exception as e:
    write_log(e)
    network_err()


def clr():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print("""
 █▄▀ █▀▀ █▀▄▀█ █▀▀ █▄░█ ▄▀█ █▀▀   ▀█▀ █▀█ ▄▀█ █░█ █▀▀ █░░
 █░█ ██▄ █░▀░█ ██▄ █░▀█ █▀█ █▄█   ░█░ █▀▄ █▀█ ▀▄▀ ██▄ █▄▄
 
 █▀ █▀▀ █▀█ ▄▀█ █▀█ █▀▀ █▀█
 ▄█ █▄▄ █▀▄ █▀█ █▀▀ ██▄ █▀▄  V1.0.0

 Coder By : https://github.com/Nux-xader
 Contact  : https://wa.me/6281251389915
 ___________________________________________________________
""")

def progress(progs, total):
    percent = 100*(progs/float(total))
    bar = '█'*int(percent)+'-'*(100-int(percent))
    print(f"\r [{bar}] {percent:.2f}%", end="\r")


def max_page(html):
    return max([int (j) for j in [i.split('">', 1)[-1].split("</a></li>")[0] for i in html.split("data-ci-pagination-pag") if "</a></li" in i] if j.isdigit()])


def get_data(page):
    global req_session
    if page == "1": url = "https://umrahcerdas.kemenag.go.id/home/travel"
    if page != "1": url = f"https://umrahcerdas.kemenag.go.id/home/travel/index/{page}"
    resp = str(req_session.get(url).text).split("<tbody>")[-1].split("</tbody>")[0]

    result = []
    for x in BeautifulSoup(resp, 'html.parser').find_all("tr"):
        row = ["".join("\n".join([j for j in str("\n".join([i for i in y.text.split("\t") if len("".join(i.split(" "))) > 0])).split("\n") if len("".join(j.split(" "))) > 0]).split("\r")) for y in BeautifulSoup(str(x.extract()), 'html.parser').find_all("td")[1:-1]]
        result.append({
            "Nama": row[0].split("\n", 1)[0], 
            "STATUS DAFTAR HITAM": row[0].split(": ")[-1], 
            "Nomor SK": row[1].split("\n", 1)[0], 
            "Tanggal SK": row[1].split("TGL SK: ", 1)[-1].split("\n")[0], 
            "Nama Direktur": row[1].split("DIREKTUR: ", 1)[-1].split("\n")[0], 
            "Alamat kantor": row[2], 
            "Akreditasi": row[0].split("Akreditasi: ", 1)[-1].split("\n")[0], 
            "Tgl Akreditasi": row[0].split("Tgl Akreditasi: ", 1)[-1].split("\n")[0], 
            "Lembaga Akreditasi": row[0].split("Lembaga Akreditasi: ", 1)[-1].split("\n")[0]
        })

    return result


def main():
    clr()
    banner()
    print(""" Menu : 
 [1] By Page
 [2] All Page
 [0] Exit""")
    while True:
        choice = str(input(" [*] Choice : "))
        if choice == "1":
            while True:
                try:
                    pages = [str(input(" [*] Page : "))]
                    if int(pages[0]) > 0: break
                except:
                    pass
                print(" [+] Invalid input")
        elif choice == "2":
            pages = [i+1 for i in range(max_page(data))]
        else:
            print(" [!] Invalid choice")
            continue

        break

    saveto = str(input(" [*] Save result to : "))
    result = []
    if saveto.split("xlsx")[-1] != "xlsx": saveto+=".xlsx"

    clr()
    banner()
    for n, page in enumerate(pages):
        print("")
        [result.append(i) for i in get_data(page) if i not in result]
        results_df = pandas.DataFrame(result)
        results_df.to_excel(saveto, index=False)
        progress(n+1, len(pages))

    print(f"\n [+] Result saved to : {saveto}")


if __name__ == "__main__":
    main()