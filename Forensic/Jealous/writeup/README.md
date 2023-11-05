# Jealous

It can be seen in the question description that the process we want to analyze further is the process related to message exchange. Of the many processes in memory, we can do a deeper analysis on the process of a chat application that is quite popular today, `LINE`.

## Analysis

When it comes to chat apps, then of course the most interesting thing is the app's chat history. So the solution to this challenge is actually quite straightforward where we only need to see chizuru's chat history. But the question is how?

Based on my analysis (sorry if there are mistakes because this is also very new to me), when we exchange messages with someone using the line application, information such as the text we sent and when we sent it is stored in ram memory.  

For more detailed artifacts, please visit the following link :
http://www.csroc.org.tw/journal/JOC30_1/JOC-3001-12.pdf


https://kinetik.umm.ac.id/index.php/kinetik/article/view/850/pdf


Thanks a lot for people who have made the above journal. I really appreciate it :D

So how do we know the chat history? To find out this, the approach taken by the author is quite simple.
1. Dump the memory of the Line.exe process
2. We need to know at least 1 message sent or received by chizuru so that we can analyze whether there is a certain order in memory for the entire chat history at that time.
3. To find this 1 message, the approach that can be taken is to execute the strings command and then grep "text" (referring to the text format in the previous journal) in the memory dump result of the Line.exe process. 
4. Once one of the messages is obtained, we can use the hexeditor to find at which offset the message appears
5. After that, we can analyze whether there is a pattern that can be utilized and voila, there is :D. The pattern that exists in memory and can be used to acquire chat history is the string "e2eeMark" in each message. My assumption is that it is a marker of end to end encryption.

Using parsingLine.py, we can retrieve chizuru's chat history (only the chats she opened).

```js
Found: b'aku cari di internet dulu deh gimana cara dekripsinya'
Found: b'hmmmm apa yak'
Found: b'9nihh yang, coba tebak ini isinya apa 17232824825695852298768761325042730018443790580293994948110228798984283575244325867896773702856809877629462993615138772470443653923033198476628704380376901745696372917716796974133419627590756466942599420161768612996890609306888809846414498468731628405084831438424000967951224503803340755900452613395984069034217434265190865864622077255260876209610854521398223331619983969822497897262970460723307887744619501229416437522226354386508669254861627656661173514599374173082540962689072991274959875912261677310542635506040797939826657842613913130222518333724037043274865434488560707165300473654533026431267493383333507468935'
Found: b'u\x0cowalaaaaaa'
Found: b'dua angka yang aku kasih itu, angka yang krusial banget lohhh'
Found: b'aku juga ga ngitung'
Found: b'hahahahahahahahh'
Found: b'berapa digit ituu kwkwkkwkwkw'
Found: b'pusing banget liatnya wkwk'
Found: b'170282656388790655154248768401706698116667930032347984458143182503761800872101670463344772387453005511384468674162653614967052322255987812198836869352275190303243091652290715686536574433316266046955987865679485777095149187534651085873864977027843827532714678284724100726197281037678509576991867720220434049417'
Found: b'waittt satu lagi'
Found: b'itu angka apa syangggg'
Found: b'\n110969371673075210314770224100258167853851056086496483043036091116549124387659481261494297101626561127887731594044363473189266039933746503506637452819333820560733383257758015593793494706877686899990580835816750128381739018243847649612394129830162401098681545483688231022305996759431601187536517073833734232743'

Found: b'Love youuuuu muachh'
Found: b'iyaaa pinter banget ayang aku'
Found: b'dua angka prima itu diperluin buat Rivest Shamir adleman'
Found: b'yappps'
Found: b'angka yang kamu bilang penting'

```

The text above is a sample of the chat line history from parsingLine.py. Unfortunately using this method still produces some duplicate messages, out of sequence, and incomplete messages so we still need to guess what is actually being discussed. As in the example above, there are some messages that are out of sequence (read from bottom to top). In this chall, I just want to insert a bit of basic RSA crypto where the values of both prime factorizations are known, and just decrypt the ciphertext. 