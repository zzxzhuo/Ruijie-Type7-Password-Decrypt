# Ruijie-Type7-Password-Decrypt
A tool to retrieve the clear text from encrypted type 7 password from equipment by Ruijie Networks
* Requirements:
```
PyQt5
```
* Usage:
```
python3 ruijie.py
```

# Description
Ruijie Networks Co., Ltd. is one of the Chinese vendor majored in enterprise networking equipment. Their device utilises a cisco-styled CLI in order to elimate the learning curve, yet share a lot of similiar functionalities with Cisco switches and routers. Cisco's IOS has a few known flaws in the scope of securing devices' configuration file, including the use of *Vigenère cipher* when encrypting user passwords. Unforunately Ruijie's implementation has the same weakness. What makes the matter worse is Ruijie's engineer decided to incorporiate the same algorithm as default cipher when configuring vty logins, web management logins, and local username/password auth db.

# Insight
There are a number of papers regarding Cisco type 7 password vulnerability, you may look into them if you are interested into greater details. To make it simple, Cisco's *Vigenère cipher* requires a constant string *c*, the algorithm pick a substring of *c* starting from some random position, trim the substring to match the length of cleartext, and do a character-by-character xor for ciphertext. Before getting saved to configuration file, prepend the picked "random position" to ciphertext.

As we may know xor is a binary operation, by performing the same calculation twice, the ouput cancels out back to orignal value. e.g. 1 XOR 0 XOR 0 = 1. Having said that, if someone somehow get hands on the constant string *c*, he/she can reverse the steps and decrypt a type 7 ciphertext.

In order to extract the constant string *c*, we first need to have some sample ciphertexts. Those 16 are encrypted form of 25 `a`s
```
004b2142423619073f022e14132604134b0c20132a2d04440028
012142423619073f022e14132604134b0c20132a2d0444002833
0242423619073f022e14132604134b0c20132a2d044400283316
03423619073f022e14132604134b0c20132a2d0444002833160e
043619073f022e14132604134b0c20132a2d0444002833160e0d
0519073f022e14132604134b0c20132a2d0444002833160e0d07
06073f022e14132604134b0c20132a2d0444002833160e0d0747
073f022e14132604134b0c20132a2d0444002833160e0d07473f
08022e14132604134b0c20132a2d0444002833160e0d07473f32
092e14132604134b0c20132a2d0444002833160e0d07473f3215
1014132604134b0c20132a2d0444002833160e0d07473f321500
11132604134b0c20132a2d0444002833160e0d07473f32150013
122604134b0c20132a2d0444002833160e0d07473f3215001333
1304134b0c20132a2d0444002833160e0d07473f321500133305
14134b0c20132a2d0444002833160e0d07473f32150013330529
154b0c20132a2d0444002833160e0d07473f3215001333052942
```
by xor'ing every one of the 25 hex value from above with alphabet `a` we can easily get string *c* implemented in Ruijie's codebase:

`*@##Wxf^cOurGer*mArKLe%aIRwolf&^StarRdH#`

# License
GPLv3
