from Crypto.Util.number import *

# flag = b'TCP1P{1_L0v3_Y0u_1n_Ev3ry_Un1v3rSe}'
# p = 110969371673075210314770224100258167853851056086496483043036091116549124387659481261494297101626561127887731594044363473189266039933746503506637452819333820560733383257758015593793494706877686899990580835816750128381739018243847649612394129830162401098681545483688231022305996759431601187536517073833734232743
# q = 170282656388790655154248768401706698116667930032347984458143182503761800872101670463344772387453005511384468674162653614967052322255987812198836869352275190303243091652290715686536574433316266046955987865679485777095149187534651085873864977027843827532714678284724100726197281037678509576991867720220434049417
# # d = 7048757320544735427480805838777356660868299051734661909704615888500764346340236544689355327353059180765172653987853865183567369217586832862927465852131519133997438490427209671518664063510210442086660326972477124619743069705383606731517285541596387513919099431153977967106578201236679763585592478005745949701002391692825267803357921034283714015199118906523287601425573705841999293708271373562480976197609340053341233730376315399345211963352523164021456908390415404022805412844459198399539113354900359434377146236262646777240589304679400769673682325357327239663286399973673312073995783431998210568747269136397518449105
# ct = 17232824825695852298768761325042730018443790580293994948110228798984283575244325867896773702856809877629462993615138772470443653923033198476628704380376901745696372917716796974133419627590756466942599420161768612996890609306888809846414498468731628405084831438424000967951224503803340755900452613395984069034217434265190865864622077255260876209610854521398223331619983969822497897262970460723307887744619501229416437522226354386508669254861627656661173514599374173082540962689072991274959875912261677310542635506040797939826657842613913130222518333724037043274865434488560707165300473654533026431267493383333507468935

# p = 110969371673075210314770224100258167853851056086496483043036091116549124387659481261494297101626561127887731594044363473189266039933746503506637452819333820560733383257758015593793494706877686899990580835816750128381739018243847649612394129830162401098681545483688231022305996759431601187536517073833734232743
# q = 170282656388790655154248768401706698116667930032347984458143182503761800872101670463344772387453005511384468674162653614967052322255987812198836869352275190303243091652290715686536574433316266046955987865679485777095149187534651085873864977027843827532714678284724100726197281037678509576991867720220434049417
# ct = 17232824825695852298768761325042730018443790580293994948110228798984283575244325867896773702856809877629462993615138772470443653923033198476628704380376901745696372917716796974133419627590756466942599420161768612996890609306888809846414498468731628405084831438424000967951224503803340755900452613395984069034217434265190865864622077255260876209610854521398223331619983969822497897262970460723307887744619501229416437522226354386508669254861627656661173514599374173082540962689072991274959875912261677310542635506040797939826657842613913130222518333724037043274865434488560707165300473654533026431267493383333507468935

p = 110969371673075210314770224100258167853851056086496483043036091116549124387659481261494297101626561127887731594044363473189266039933746503506637452819333820560733383257758015593793494706877686899990580835816750128381739018243847649612394129830162401098681545483688231022305996759431601187536517073833734232743
q = 170282656388790655154248768401706698116667930032347984458143182503761800872101670463344772387453005511384468674162653614967052322255987812198836869352275190303243091652290715686536574433316266046955987865679485777095149187534651085873864977027843827532714678284724100726197281037678509576991867720220434049417
ct = 17232824825695852298768761325042730018443790580293994948110228798984283575244325867896773702856809877629462993615138772470443653923033198476628704380376901745696372917716796974133419627590756466942599420161768612996890609306888809846414498468731628405084831438424000967951224503803340755900452613395984069034217434265190865864622077255260876209610854521398223331619983969822497897262970460723307887744619501229416437522226354386508669254861627656661173514599374173082540962689072991274959875912261677310542635506040797939826657842613913130222518333724037043274865434488560707165300473654533026431267493383333507468935

n = p * q
totient = (p - 1) * (q - 1)
e = 65537
d = pow(e, -1, totient)
# print(d)
# ct = pow(bytes_to_long(flag), e, n)
# assert ct == ct1
# print(ct)
print(long_to_bytes(pow(ct, d, n)))

# print(isPrime(bytes_to_long(p)))