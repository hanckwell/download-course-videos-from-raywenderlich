# RayWenderlich-Crawler


## Usage

Requires subscription to download course videos from RayWenderlich.

1. Open Chrome Developer Tools, switch to 'Network' tab.

2. Access a video course page on raywenderlich.com (e.g. `https://videos.raywenderlich.com/courses/91-your-first-swift-4-ios-11-app/lessons/1`).

3. Right click on the first GET request, select Copy -> Copy as cURL. The copied value should look like:

```
curl 'https://videos.raywenderlich.com/courses/91-your-first-swift-4-ios-11-app/lessons/1' -H 'Pragma: no-cache' -H 'DNT: 1' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja-JP;q=0.6,ja;q=0.5' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Cache-Control: no-cache' -H 'Cookie: ...' -H 'Connection: keep-alive' --compressed
```

4. Replace the "..." in rwcrawl.py (variable str_curl) with the copied value.

5. Replace the video course URL (`https://videos.raywenderlich.com/courses/91-your-first-swift-4-ios-11-app/lessons/1` in our example) with `%s`. The result in the Python source code should look like:

```
str_curl = "curl '%s' -H 'Pragma: no-cache' -H 'DNT: 1' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja-JP;q=0.6,ja;q=0.5' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Cache-Control: no-cache' -H 'Cookie: ...' -H 'Connection: keep-alive' --compressed"
```

6. Download the entire course using command:

```
python3 rwcrawl.py https://videos.raywenderlich.com/courses/91-your-first-swift-4-ios-11-app/lessons/1
```

You can download other video courses with this command as well, just replace the URL with other courses'.

Enjoy.

