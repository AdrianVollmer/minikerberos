from pprint import pprint
from minikerberos.crypto.hashing import md4
from minikerberos.protocol.asn1_structs import *
from minikerberos.protocol.encryption import Key, _enctype_table, _HMACMD5, cf2
from minikerberos.protocol.constants import EncryptionType
from minikerberos.common.creds import KerberosCredential


def decrypt_authenticator(authenticator_enc_type, authenticator_enc_data, key_bytes, key_usage = 11):
	cipherText = authenticator_enc_data
	kerberos_key = Key(_enctype_table[authenticator_enc_type].enctype, key_bytes)
	authenticator_data_dec = _enctype_table[authenticator_enc_type].decrypt(kerberos_key, key_usage, cipherText)
	authenticator_dec_native = Authenticator.load(authenticator_data_dec).native
	return authenticator_dec_native


asreq_1 = bytes.fromhex('3081f5a103020105a20302010aa32c302a3011a10402020080a20904073005a0030101ff3015a104020200a7a20d040b3009a00703050080000000a481ba3081b7a00703050040810010a11b3019a003020101a11230101b0e6f76657270726f74656374656424a20b1b09746573742e636f7270a31e301ca003020102a11530131b066b72627467741b09746573742e636f7270a511180f32303337303931333032343830355aa611180f32303337303931333032343830355aa70602045ef7d529a81530130201120201110201170201180202ff79020103a91d301b3019a003020114a11204104f56455250524f544543544544202020')
kerr_1 = bytes.fromhex('7e81c33081c0a003020105a10302011ea411180f32303231303332363134333631335aa505020309e5d3a603020119a90b1b09746573742e636f7270aa1e301ca003020102a11530131b066b72627467741b09746573742e636f7270ac68046630643041a103020113a23a04383036302da003020112a1261b24544553542e434f5250686f73746f76657270726f7465637465642e746573742e636f72703005a0030201173009a103020102a20204003009a103020110a20204003009a10302010fa2020400')

asreq_2 = bytes.fromhex('30820143a103020105a20302010aa37a3078304ca103020102a24504433041a003020112a23a04380290feb9048406b4acf9294b24d265d73498f7c09e5d2198ae694dc3c2e8d0e5cad9c18b75b950a3c65606c2623edce7e62da102b00e09493011a10402020080a20904073005a0030101ff3015a104020200a7a20d040b3009a00703050080000000a481ba3081b7a00703050040810010a11b3019a003020101a11230101b0e6f76657270726f74656374656424a20b1b09746573742e636f7270a31e301ca003020102a11530131b066b72627467741b09746573742e636f7270a511180f32303337303931333032343830355aa611180f32303337303931333032343830355aa70602045ef7d5cea81530130201120201110201170201180202ff79020103a91d301b3019a003020114a11204104f56455250524f544543544544202020')
asrep_2 = bytes.fromhex('30820640a003020105a10302010ba23e303c303aa103020113a2330431302f302da003020112a1261b24544553542e434f5250686f73746f76657270726f7465637465642e746573742e636f7270a30b1b09544553542e434f5250a41b3019a003020101a11230101b0e4f56455250524f54454354454424a58204586182045430820450a003020105a10b1b09544553542e434f5250a21e301ca003020102a11530131b066b72627467741b09544553542e434f5250a382041a30820416a003020112a103020102a282040804820404e00661aa6cec28a32b9441f9841398c31645e4a70ff778efa2cb87776dcfcd6eed5726121ec3c07352495cc1fa20a914ceb7aeda95bb691f5d9af6f693b3b264a20eb1b14f9884822898dd0ce3f70597bd8b8d86f3ca0180de4687a26f4c5011ee81ee2e7c3cab483a8873e3eb59c44c394eed5c6deb7dc3cf35560d750bb0efbbcd33f7146f8291352349f664d33a08dc437cc6ee1480cb4554b1e798fb806155e9ec4aed2385bf244e0488d28e64144b28df0e50f7245719c096061021758dcbac01d902491fdb81333d366461ac2ad7dceb6151faa56718406f13ee8a6334c292ae8bffe918d7aa22d5becd179699851a630648237c6a16fee56525bc44ce6f8fd526a6278c077e8b37e8dfb841ad538a4e3436e0aa469c8b581589c6452cd881c3ec8029db8f5a5984c14657c5fc9aa063cb9107b325076fe985ab26656866a32f0101c16779e3de9cfa5cdd33d29cc3e9f98b0a31670e05d5b21d5ac6db5e42ca73c6aef2c003e624327571f77f62c9f8ce7ca978346e9d5cc2017648bc9254c53dbb3514381450821c52acf0f97d3dc2593be829f56335ed8187e3fad117b35e1245c1ee16f50cc7d8c296137fcba0d761b4cbf76ceb8bbb64934c60382ab1645c2980bfdaa5bc5940013b006b419e0649645a0bb1e8288b69b83cd51c152da8ca1621d89e2eb9bc96481a67a19327552b71b33669edfe9b878e4496f1174df6f570eb7533b102e5256326168bd61107e27967176e6053a159b261b2628dd666f05837f894f6d975022541e591cfb562a5efaaaa581e68fe446eed144c5559e73f3313cbb70ef3924495690d799ab8deb57b1559dc045db060c664b1ba016c0b79ad9bb9f5bbcc0c0388deaa32cdbbb32ec213dc7da036b6ff4f4c1cd24a947764109b11ebdaf5f07ee1d5d6436f34bc6e7033272ed4d0206c5c0969e65020effa8378a4140916f384c9b941aeb0a22a38d27115eaf82c261068b2390374fe7fccd811fcde57b912b19b40436ca5b3180540d2873f988df36d72db7e32855b59e614b9d90f4b8770ab83795b0fe855e56f7cd9a43e6207b3593e825b4f711e10c28aa436520ed43bf49367c445380123d86a4a7f6d53cb9ecc72929f313ed96c4d8a7b28302437b09af0c143cd84bb70553cc4c031c88e3cb7ca36bb3b755677a6cf3a2594c5283751d97a0f5c5ba1b865f105c03791d075afea81f2dc1da50e9056b69d69ae6f163d80af9c81154df2a4887a7ec1abe642a08338cbaf2ade5ec555badbc7fb5bfab57319f0471a8b0570abf6abf20a8e051c97bff807e97634b75d8ef0fff5ec98a053107c57635b976e36b9e5b39eac3882b697a7bdf9c2c7be2e84728d61b8ac3b79a6674c0ff57c0eba1bf78f4af86c526b04a6a81f61e49fa309922dcd14e7ff0e39651b696a6308362d777a2c0434e8d2ab426b557aa329a682016c30820168a003020112a103020104a282015a04820156edae2f7ff0210be88cc8e72bd4e6d9535129d56a52cc15795abacf199c343afe610a1087e820272e9bcbf02dcb7a009929c555ea6d32db1ccba176e9723e7161526e84963fe8dd1f2f4c69754190410b307be7b60fb60ac37aa79e776e5f5fd7aae8a5cc2243b61a1d3b0b4259dd56b516dad275ce97f02992304874e4a4615b1d0f979ff7c2df36e66e41586043658cab0297ed3d8ce637374d1b8066478fd103ae4b7c9ff28cd3b17effff2b8aa8720c571f04300a1c360fe18af6d2a19953ce12a36217b7a4471db2a28f76ed1e4180f8391afe87186525f7a370249643bb98d1bedda357ee14ab95083aa30b47f492ad6a0092cf44ea8ae272746493be7158565214aabbcd8aca23823e21c49490cce58372611c219d7e9399db5aea221804ef8a33a6a2b949c38931d2bca46ec285328fc19484a3e731b12945b1e5e5241fbc7b0d8dfdbae4bb30bbd253f00bf4644c1f716b44')



asreq_3 = bytes.fromhex('3081f5a103020105a20302010aa32c302a3011a10402020080a20904073005a0030101ff3015a104020200a7a20d040b3009a00703050080000000a481ba3081b7a00703050040810010a11b3019a003020101a11230101b0e6f76657270726f74656374656424a20b1b09544553542e434f5250a31e301ca003020102a11530131b066b72627467741b09544553542e434f5250a511180f32303337303931333032343830355aa611180f32303337303931333032343830355aa70602045ef56e29a81530130201120201110201170201180202ff79020103a91d301b3019a003020114a11204104f56455250524f544543544544202020')
kerr_3 = bytes.fromhex('3081c0a003020105a10302011ea411180f32303231303332363134333631335aa50502030a2429a603020119a90b1b09544553542e434f5250aa1e301ca003020102a11530131b066b72627467741b09544553542e434f5250ac68046630643041a103020113a23a04383036302da003020112a1261b24544553542e434f5250686f73746f76657270726f7465637465642e746573742e636f72703005a0030201173009a103020102a20204003009a103020110a20204003009a10302010fa2020400')

asreq_3 = bytes.fromhex('30820143a103020105a20302010aa37a3078304ca103020102a24504433041a003020112a23a043861cdf95df275ca3da7a9fae5527e2812463bb4ae0b3156d2186fead88305219c49e61c49c572f046ed663b46c2b22fbdbf7e7b4860063ad43011a10402020080a20904073005a0030101ff3015a104020200a7a20d040b3009a00703050080000000a481ba3081b7a00703050040810010a11b3019a003020101a11230101b0e6f76657270726f74656374656424a20b1b09544553542e434f5250a31e301ca003020102a11530131b066b72627467741b09544553542e434f5250a511180f32303337303931333032343830355aa611180f32303337303931333032343830355aa70602045ef56e2ca81530130201120201110201170201180202ff79020103a91d301b3019a003020114a11204104f56455250524f544543544544202020')
asrep_4 = bytes.fromhex('6b82064430820640a003020105a10302010ba23e303c303aa103020113a2330431302f302da003020112a1261b24544553542e434f5250686f73746f76657270726f7465637465642e746573742e636f7270a30b1b09544553542e434f5250a41b3019a003020101a11230101b0e4f56455250524f54454354454424a58204586182045430820450a003020105a10b1b09544553542e434f5250a21e301ca003020102a11530131b066b72627467741b09544553542e434f5250a382041a30820416a003020112a103020102a2820408048204048c76c7670f689ef1742dedd3c16c0043521cf2a3ca5f6fef84b760e97a452ef70ad69d028cd0c0aa1d0692421b74f7c102d338e35ebcba3d96554bc013a3f23d841cc570506d457acd7a519e79c32fc3ac443b687599be74ce59346aba831983d8da4a24e5c1d8d0758bae89cc34ecdd1754e51bb527c7171086897faa611b6f5f501eebf0a488cd4b07e0c7859c67cc000dce6b9c8945c3ead8d6786663ab585b30e86f51935e6ac5a0c813c567d03d2d9a6ad7b67d2f77098582bd80e0c81c1367f865f41a027d628ac4874036e0face8362c2375fedabcbf6ca98a02dd693cfa96d840367b15a02a3582abbee29d70a55d785f50370fc0e1b6ba349dc3c79d498fbc46ce4f3947ae94c4d9f5c2791ec4824835c55f34983aa30cb22d892b4764f4746c8e9231ada10c9eb3dfdb3ad21c89102d009539164e5f64b79490605954f5298bcf7eaedb1498620a5f06f075be7f1d6ca22a4a788a9af7e4f8ee4202951a5511d62b99177893102c5654b7cdd3d402b44105fe4daaca98429cac4eb51fa7879512427a813db032a610724ea8648263f592c2f4dd934f2b7e53419c75b371e6a7dc9636d2538a8cd74e36041e8755c018eb9d51b1f4e5ea25db3c576c8a9db7b6c019f9ae550f0704b2eaaae489bf42274217982063fc6498fe638698feab668a8f4a189dc7b762bc79eda23be1afbee6717930dca827d270d220a265d7dc25d31ca54b24e518c5f6a95ed3b53adc4512838d63c75d037b75049fc604f92620e46f1a9ba49fae3015c0431c57e7981bb7a97f3115ea865206ada7300e2ff1c87728c587fb64f6d31ef746623d454bafb54fb451eb5bdae84ef445483a255f20eb28a345afc245f8fea7eefca583379c2935b9f6b31c759a2ca1b1d7df33c86b187e56aa8dd6edb139bc4d26a53cce1d236a18276e32c135d05fbc36e3d9c310cb36892fc2c9d7716bb3fae2b788986869d92af5379d5e5e334b00b31bbc0f7f1957051c144b45f297a0bb2ce07c1f65d57931662cc3aea530bc4f0228c6653effde024e0a4096ba5e0ad5b8964a2042733ce290c36e604820a6f9be00aa4652f119a0972763ed264d45675b10cc025633fcf873d10bc2855086e8beaf428c6ee9f16e93718477f21b643eb2459b5222587395e8d5da9f6d31ffee7088295e65de747823e74da93df9a35eabbf93f7267ea79f0557fb8896f9004af99f42aed55510d169bbabd3e0bd4c517fa30bb396e31182685479ef96b78146a40597927d62d9fc044d257b63e7db6977598871f755ef36b5b9ff4b9ef1e6cb2255a51c57f408f89df9ad50b7ef2d243ca86b0fe0376c47813e305463d6aa081e70ee9f4f677934f74018b8d0a701e4d4c080ae61b698d78b3a5bb116035b52c0575878bb29b4b91848e84844b6e7118086e639ace845bc028cac48c8765fcf0970ee045a2a682016c30820168a003020112a103020104a282015a048201565bcb73bbb09543ebe6e4c5d3c96d3f920d8b95e7d0e25f120945cbec4f7db922d9be59de2834f135eb330e0dd8269d1e9406fa73f663a76090761dbe334736e8db15fa20bcfa0d564c401bffe53dc4f021ee7ad3210e6dfc8853626975e9f94dc56cb349dfcb98a2defff200f1794f751f6d1f9cce219413d5744cd1496edfaa45d28e5a5debc50f9cb4d179b09f5bb97c2a6b9e3a8fed5456505aa817a9c3635c94034032690002714b0838d66a6fc85e1d7a3a4cee18afbeb1ac0f59127151dfac9f5efc1ca3c2b2d14de36d015b1cc8937ee1304373252c973dba5007f3923b959a6e6c9cdb29d0b5848a14d6da45e6f25f6b5ccee0f81274bde93c1df34d739ee07eb202b7310eb51a06e5abf39f697fe84de945889e253ebedd4b334a0cb5a3cb6a253a8361ad8bfbbc96dce05c7e0b017f8039567198d316b10fbaf6e8c83cfc66eb43c5f71605e78dd3a044369f977e8c494a')


asreq_1_native = KDC_REQ.load(asreq_1).native
#pprint(asreq_1_native)

kerr_1_native = KerberosResponse.load(kerr_1).native
pprint(kerr_1_native)

print('============= ERROR E-DATA =======================')
# if error is KDC_ERR_PREAUTH_REQUIRED then e-data might contain info. this info is 
kerr_1_edata_native = METHOD_DATA.load(kerr_1_native['e-data']).native
pprint(kerr_1_edata_native)


asreq_2_native = KDC_REQ.load(asreq_2).native 
pprint(asreq_2_native)

#print('aaa')
#pprint(asreq_2_native['padata'][0]['padata-value'])

asrep_4_native = KerberosResponse.load(asrep_4).native
pprint(asrep_4_native)

cred = KerberosCredential()
cred.username = 'hostoverprotected.test.corp'
cred.domain = 'TEST.corp'
#cred.password = 'Passw0rd!1'
cred.kerberos_key_aes_256 = '7289306c73ca8909cf89bc01afe3e29f26211f89d922fb317cc5d81cfdf8465d'

supp_enc = EncryptionType.AES256_CTS_HMAC_SHA1_96

cipherText = asrep_4_native['enc-part']['cipher']
print(cipherText.hex())
key_bytes = cred.get_key_for_enctype(supp_enc, None)
kerberos_key = Key(_enctype_table[asrep_4_native['enc-part']['etype']].enctype, key_bytes)
temp = _enctype_table[asrep_4_native['enc-part']['etype']].decrypt(kerberos_key, 3, cipherText)

temp_dec = EncASRepPart.load(temp).native
pprint(temp_dec)

computer_session_key_bytes = temp_dec['key']['keyvalue']



#### decrypting authenticator (it's in the second AP_REQ message FAST data's armor section that is for the user)
#### includes a ticket with an authenticator



data = bytes.fromhex('6e82051d30820519a003020105a10302010ea20703050000000000a38204586182045430820450a003020105a10b1b09544553542e434f5250a21e301ca003020102a11530131b066b72627467741b09544553542e434f5250a382041a30820416a003020112a103020102a2820408048204048c76c7670f689ef1742dedd3c16c0043521cf2a3ca5f6fef84b760e97a452ef70ad69d028cd0c0aa1d0692421b74f7c102d338e35ebcba3d96554bc013a3f23d841cc570506d457acd7a519e79c32fc3ac443b687599be74ce59346aba831983d8da4a24e5c1d8d0758bae89cc34ecdd1754e51bb527c7171086897faa611b6f5f501eebf0a488cd4b07e0c7859c67cc000dce6b9c8945c3ead8d6786663ab585b30e86f51935e6ac5a0c813c567d03d2d9a6ad7b67d2f77098582bd80e0c81c1367f865f41a027d628ac4874036e0face8362c2375fedabcbf6ca98a02dd693cfa96d840367b15a02a3582abbee29d70a55d785f50370fc0e1b6ba349dc3c79d498fbc46ce4f3947ae94c4d9f5c2791ec4824835c55f34983aa30cb22d892b4764f4746c8e9231ada10c9eb3dfdb3ad21c89102d009539164e5f64b79490605954f5298bcf7eaedb1498620a5f06f075be7f1d6ca22a4a788a9af7e4f8ee4202951a5511d62b99177893102c5654b7cdd3d402b44105fe4daaca98429cac4eb51fa7879512427a813db032a610724ea8648263f592c2f4dd934f2b7e53419c75b371e6a7dc9636d2538a8cd74e36041e8755c018eb9d51b1f4e5ea25db3c576c8a9db7b6c019f9ae550f0704b2eaaae489bf42274217982063fc6498fe638698feab668a8f4a189dc7b762bc79eda23be1afbee6717930dca827d270d220a265d7dc25d31ca54b24e518c5f6a95ed3b53adc4512838d63c75d037b75049fc604f92620e46f1a9ba49fae3015c0431c57e7981bb7a97f3115ea865206ada7300e2ff1c87728c587fb64f6d31ef746623d454bafb54fb451eb5bdae84ef445483a255f20eb28a345afc245f8fea7eefca583379c2935b9f6b31c759a2ca1b1d7df33c86b187e56aa8dd6edb139bc4d26a53cce1d236a18276e32c135d05fbc36e3d9c310cb36892fc2c9d7716bb3fae2b788986869d92af5379d5e5e334b00b31bbc0f7f1957051c144b45f297a0bb2ce07c1f65d57931662cc3aea530bc4f0228c6653effde024e0a4096ba5e0ad5b8964a2042733ce290c36e604820a6f9be00aa4652f119a0972763ed264d45675b10cc025633fcf873d10bc2855086e8beaf428c6ee9f16e93718477f21b643eb2459b5222587395e8d5da9f6d31ffee7088295e65de747823e74da93df9a35eabbf93f7267ea79f0557fb8896f9004af99f42aed55510d169bbabd3e0bd4c517fa30bb396e31182685479ef96b78146a40597927d62d9fc044d257b63e7db6977598871f755ef36b5b9ff4b9ef1e6cb2255a51c57f408f89df9ad50b7ef2d243ca86b0fe0376c47813e305463d6aa081e70ee9f4f677934f74018b8d0a701e4d4c080ae61b698d78b3a5bb116035b52c0575878bb29b4b91848e84844b6e7118086e639ace845bc028cac48c8765fcf0970ee045a2a481a73081a4a003020112a2819c048199f363e352e88f51743ffa449016a24aeab84f4be14dc24216bfa48837cc4c0c3327580a0caa498e8674d283711bae53eceb367b03e39b3975fb76b820f053f5c2830bdc2fc672d30be07fce88a7bfad85ad5f1470594db2c61b725223103eb3a08de787d3eabbc9a395eb4fabe3062dde554fa8825629fd395903377a095e64c58e22d114aea20741d1717c394353f8696888b4b9308bd1f4e1')
d_native = AP_REQ.load(data).native
pprint(d_native)
pprint(d_native['authenticator']['cipher'].hex())
cipherText = d_native['authenticator']['cipher']

kerberos_key = Key(_enctype_table[d_native['authenticator']['etype']].enctype, computer_session_key_bytes)
temp = _enctype_table[d_native['authenticator']['etype']].decrypt(kerberos_key, 11, cipherText)

temp_dec = Authenticator.load(temp).native
pprint(temp_dec)

computer_subkey_type = temp_dec['subkey']['keytype']
computer_subkey_bytes = temp_dec['subkey']['keyvalue']


client_cred = KerberosCredential()
client_cred.username = 'victim'
client_cred.domain = 'TEST.corp'
#client_cred.password = 'Passw0rd!1'
client_cred.kerberos_key_aes_256 = 'ef7dfcbdeb556d46d3adeb8e5ca3a6ef562ad065d4f8b0ec65e16d3612df8ec1'


def decrypt_fast_as_req(session_key):
	#### trying to decrpyt the AS-REQ with user's password + tgt subkey key from the machine account
	client_as_req = bytes.fromhex('6a8207903082078ca103020105a20302010aa38206d3308206cf308206cba10402020088a28206c1048206bda08206b9308206b5a08205323082052ea003020101a1820525048205216e82051d30820519a003020105a10302010ea20703050000000000a38204586182045430820450a003020105a10b1b09544553542e434f5250a21e301ca003020102a11530131b066b72627467741b09544553542e434f5250a382041a30820416a003020112a103020102a2820408048204048c76c7670f689ef1742dedd3c16c0043521cf2a3ca5f6fef84b760e97a452ef70ad69d028cd0c0aa1d0692421b74f7c102d338e35ebcba3d96554bc013a3f23d841cc570506d457acd7a519e79c32fc3ac443b687599be74ce59346aba831983d8da4a24e5c1d8d0758bae89cc34ecdd1754e51bb527c7171086897faa611b6f5f501eebf0a488cd4b07e0c7859c67cc000dce6b9c8945c3ead8d6786663ab585b30e86f51935e6ac5a0c813c567d03d2d9a6ad7b67d2f77098582bd80e0c81c1367f865f41a027d628ac4874036e0face8362c2375fedabcbf6ca98a02dd693cfa96d840367b15a02a3582abbee29d70a55d785f50370fc0e1b6ba349dc3c79d498fbc46ce4f3947ae94c4d9f5c2791ec4824835c55f34983aa30cb22d892b4764f4746c8e9231ada10c9eb3dfdb3ad21c89102d009539164e5f64b79490605954f5298bcf7eaedb1498620a5f06f075be7f1d6ca22a4a788a9af7e4f8ee4202951a5511d62b99177893102c5654b7cdd3d402b44105fe4daaca98429cac4eb51fa7879512427a813db032a610724ea8648263f592c2f4dd934f2b7e53419c75b371e6a7dc9636d2538a8cd74e36041e8755c018eb9d51b1f4e5ea25db3c576c8a9db7b6c019f9ae550f0704b2eaaae489bf42274217982063fc6498fe638698feab668a8f4a189dc7b762bc79eda23be1afbee6717930dca827d270d220a265d7dc25d31ca54b24e518c5f6a95ed3b53adc4512838d63c75d037b75049fc604f92620e46f1a9ba49fae3015c0431c57e7981bb7a97f3115ea865206ada7300e2ff1c87728c587fb64f6d31ef746623d454bafb54fb451eb5bdae84ef445483a255f20eb28a345afc245f8fea7eefca583379c2935b9f6b31c759a2ca1b1d7df33c86b187e56aa8dd6edb139bc4d26a53cce1d236a18276e32c135d05fbc36e3d9c310cb36892fc2c9d7716bb3fae2b788986869d92af5379d5e5e334b00b31bbc0f7f1957051c144b45f297a0bb2ce07c1f65d57931662cc3aea530bc4f0228c6653effde024e0a4096ba5e0ad5b8964a2042733ce290c36e604820a6f9be00aa4652f119a0972763ed264d45675b10cc025633fcf873d10bc2855086e8beaf428c6ee9f16e93718477f21b643eb2459b5222587395e8d5da9f6d31ffee7088295e65de747823e74da93df9a35eabbf93f7267ea79f0557fb8896f9004af99f42aed55510d169bbabd3e0bd4c517fa30bb396e31182685479ef96b78146a40597927d62d9fc044d257b63e7db6977598871f755ef36b5b9ff4b9ef1e6cb2255a51c57f408f89df9ad50b7ef2d243ca86b0fe0376c47813e305463d6aa081e70ee9f4f677934f74018b8d0a701e4d4c080ae61b698d78b3a5bb116035b52c0575878bb29b4b91848e84844b6e7118086e639ace845bc028cac48c8765fcf0970ee045a2a481a73081a4a003020112a2819c048199f363e352e88f51743ffa449016a24aeab84f4be14dc24216bfa48837cc4c0c3327580a0caa498e8674d283711bae53eceb367b03e39b3975fb76b820f053f5c2830bdc2fc672d30be07fce88a7bfad85ad5f1470594db2c61b725223103eb3a08de787d3eabbc9a395eb4fabe3062dde554fa8825629fd395903377a095e64c58e22d114aea20741d1717c394353f8696888b4b9308bd1f4e1a1173015a003020110a10e040c5783dcf20fb734229e49def5a28201623082015ea003020112a282015504820151883af50c6bc8bd5ba10a4ed6688ad248057271a5b06405639631c7ca00311f005f6932155536d5e80ed9ef398589703a24c6093415d8c7e1b5a6bd0c47f501b290e6ca0d9f0d8dd3d61fc04090dae610e4e92cbfd9b1568dfb80058a76897065a262ffca403c62b7442ce419936a3b7a8581cbb3f61e09fa0d5dc1f0d9444fb65f3090013d1377a8438e0de04a8c81805131e882985e112204639bcc24ef66624a31b8121fdc3c357b2c389f98523d1ffbeae85a38a3b461cdd6160f518faf86b9f83f95cfe8217dcae43c062405328791368d84674eea1c3d32801e38e96fde33fbb8cff068149b3d668b0720ec3bd90a69fb77965f6b092c4d93f7bc341a1abef7c1bda73680251ddc7f58643a92108ce7fdcfe07e0ae4f12f751b1a1d01b1d450699df65a2fcfb9144ca25ad45bf5eec2402166978114526ff97d5e05b5f0487a612bab979d00cfe08ee5e3e5ea7b5aa481a83081a5a00703050040810010a1133011a003020101a10a30081b0676696374696da2061b0454455354a3193017a003020102a110300e1b066b72627467741b0454455354a511180f32303337303931333032343830355aa611180f32303337303931333032343830355aa706020461d2923ea81530130201120201110201170201180202ff79020103a91d301b3019a003020114a11204104f56455250524f544543544544202020')
	client_as_req_native = AS_REQ.load(client_as_req).native

	encfastreq = None
	armor_native = None # at this point this is a AS_REP ticket which was obtained using the machine account. This ticket is used here to identify the correct sub-key to be used.
	for padata in client_as_req_native['padata']:
		if padata['padata-type'] == 136:
			armoreddata = PA_FX_FAST_REQUEST.load(padata['padata-value']).native
			encfastreq = armoreddata['enc-fast-req']
			armortype = armoreddata['armor']['armor-type']
			if armortype != 1:
				raise Exception('AS_REQ must have armortype = 1')
			armor_native = AP_REQ.load(armoreddata['armor']['armor-value']).native




	#### First we need to obtain the subkey from the 'armor' part of the PA-FX-FAST PADATA section. This is actually an AP_REQ structure that holds the Authenticator (encrypted with the TGT session key recieved using the machine account) which holds the subkey. This subkey is used together with the machine account session key to form the armorkey.
	
	
	authenticator = decrypt_authenticator(armor_native['authenticator']['etype'], armor_native['authenticator']['cipher'], session_key)
	computer_subkey_type = authenticator['subkey']['keytype']
	computer_subkey_bytes = authenticator['subkey']['keyvalue']



	#### now that we have the subkey, we can create the armor-key and using it we can decrypt the KrbFastReq structure which will contain the (normal) AS_REQ with the encrypted timestamp used for preauth
	cipherText = encfastreq['cipher']
	computer_session_key = Key(_enctype_table[encfastreq['etype']].enctype, session_key)
	client_authenticator_subkey = Key(_enctype_table[encfastreq['etype']].enctype, computer_subkey_bytes)

	armor_key = cf2(encfastreq['etype'], client_authenticator_subkey, computer_session_key, b"subkeyarmor", b"ticketarmor")

	krbfastreq_dec_data = _enctype_table[encfastreq['etype']].decrypt(armor_key, 51, cipherText)
	krbfastreq_dec = KrbFastReq.load(krbfastreq_dec_data).native
	
	pprint(krbfastreq_dec)
	print('krbfastreq_dec sucsess dec')

	return armor_key.contents, decrypt_fast_as_req


def decrypt_fast_as_rep(armor_key_bytes, computer_subkey_bytes):
	asrep_data = bytes.fromhex('6b8207333082072fa003020105a10302010ba282015b3082015730820153a10402020088a282014904820145a08201413082013da082013930820135a003020112a282012c04820128b481f8034f43c667939a3a0a8459c05163929b8d3e7e95f5ac52a285766281a4e5fa9c8961cd4588b651b8ca518203b326049e8ee73faa619bd06473d98fe22f6f0ae2e3adf4a40794ed83d9b4821d3268352e0a1ff24624bbdb58f91f71230b3cdf26a69b4219791343eef6c8473ea6263531ddf54256537bdde322b0fc18838f4a5399cd812fbd972595c75db02e078dc2a2f53335b7d824176d96d0abc5a1f26559667b6dcc180c0321d68222dfdc0dc15d325c33d1536f97e6c8a53e1b7d421884cc6ea64e2f4689621179121394e9e97fda6072cfd34d9f32025672d8f0ecce9bf7ec9e2144dea29673cd2cba5491c47c8603ba05a894fa92ffa1d758109d60f05b2c984a918d4d0830a732eb3aaddb967483588d918794f6a9f38da74b0415d3866e1abd94a30b1b09544553542e434f5250a4133011a003020101a10a30081b0676696374696da58204306182042c30820428a003020105a10b1b09544553542e434f5250a21e301ca003020102a11530131b066b72627467741b09544553542e434f5250a38203f2308203eea003020112a103020102a28203e0048203dce5f6db8e3c92a1f857ed0002a7ed9a30f85ef0aa9e08560e0128b17508ca36eda097ac98266da80129d578bd8af033b8378db62d256a50e665f0cdcf8175eb5fcf9a37fe101ecf816c6206595ac612b52680cf2a29aed78b68b56aae12c3367a79d5f3dd973d8cefb6ebc53ed9e1768ebb71e11f980ee75818bd86cdcd8213c1b12314b592429ea0975adc70cff2e871e12f60ecf8c1a05b95c280be491eb61bf5bab8603e9e60a8eafd16650deaac640a4f26de115d2837e1078a758129bc2d479c63534b44dfebbbdbfc8e5002017c46a1d1bd6066d7d28e902bb4b59800f9dcac9dd3a39d47d413daaf5f97e19ae125a9e547122b04abb7b05d4d72bafbd154c5407d7caa8d861e2ea64ee0fdcc8f1d777734f32cdad37898049bcc23c84968101738e887678238099d21ab14e10562d6c11933ff288394a4e3f501a078faff41eea0567262f304842796a913a6d3e4c845cd7f919da7702ea4077a71acac00778ce2994a10acc38bc9a1f88dc86f8646a08877af8708404d5bebf180986a9518d40e3f8bbffd324372617531f9a541b1f12c25fe680e29d5e6ea7cf4efca55848c9719f880099bfda9d8363db1847ad570cc9d110cce8fbd1073adea8a1d000482930c07e91e9e1791dc85caf267ea9a6dd69151ad8d542aca85ed3cb106eed8f173acddb7313b71a99f9cb490ec98cbd38e18504db29ae0f3b5d14602593730e9e5acacc49b892e7257dcf01cf68d08f921e9ae2c8ebbe790887a2038505f00f8fd9281581415096450a591af4f993b10f11dbf74598614e706664ba398b065f9263f0fd92e210575c647b3571147e207f3af51cd990a6bdfb501de55a15e6be55c63435bfc8336dfb367a7ea9b0673bfaafe9eeb67fd3e78aa5fd57f662449ce2be1032693504b3277da419a2dc20c28d3481bd4e2a02a3a23bfd690634cd596b22a34af1514c9a28ae8daa5757ad25a8d9f871ea5b9ea613171e1949f322045309877fa930cf5cb39c144e960b7e2a27d5a1dac8e7857c0cdc5548502b9352c0d3d71ba7a24a1fb3bc8dcf5786750abf8b57caeca7e9854e84c3fd85fe561c78568879191e29388d246185d4e9fd9e85907a71830bbe63a7270ad68523f940507ae322a7750c5f3aeda561b1bb3aed043557fc5023b1eba66db649753bb3099a9fde06be697c743a0954825c5ae4b3eab89ba86893365b65a9267f3b0c52a0198952512d12d044f47db039b0feba44f0d4cdc2c2aaab9dd86c568c73afa48d518e3e22b208d48d712554f11eedc5af8df587352d521dcb1c7bc52533f4752b477f922021777c014648853090202df6c7bcdd15329e83eb0688e0dafd0e7f4dcd5a5c27c9f2c1ea2d84d952a46c63398400b2d84ca322ea9b5a682016c30820168a003020112a103020103a282015a048201560efd8839a038e5399968a534391f82ce15d602d3195d26c7bcc6d954980c1fe80cb83d220610553a87e352899542077e4cd431b2cb0e4944eae0c8c85c3e7214a479220c84da70c4a48d8b4dc3ea8c9da34ee36c775b7b30a227c311f2a5ed8046a98d87d2ae113fbc37c0283a46ea50ba9bc0f33d902f7649350b6120ff794e3f6a4608f3ec482fe45001b442958bed6da03a5518a701180f49c215edd8a1c38865a33cff928bb1b82819986326bb572122cc9f7bdab019175a73c0b3aa85df44e1ca2c1d516eeeba17443ea28d019136bef31d6b14a600db9d8211ba9827ba54fc1df68286060dff2a89bd4653c0b18a135d15dd922bc390cadd0c5fe7592ad97bdd1387c5269351bcaa4f6043cd3cad3fbbd577648ee2d9e32711c24d1739e004b1241b9d7caa1007c3d81999a01238362a7d680153301c6562aa523b8673afc5571d96c3afad8e01f390ef14d48dc2843182eab9')
	asrep = AS_REP.load(asrep_data).native

	encfastrep = None
	for padata in asrep['padata']:
		if padata['padata-type'] == 136:
			armoreddata = PA_FX_FAST_REPLY.load(padata['padata-value']).native
			encfastrep = armoreddata['enc-fast-rep']

	cipherText = encfastrep['cipher']
	armor_key = Key(_enctype_table[encfastrep['etype']].enctype, armor_key_bytes)
	krbfastrep_dec_data = _enctype_table[encfastrep['etype']].decrypt(armor_key, 52, cipherText)
	krbfastrep_dec = KrbFastResponse.load(krbfastrep_dec_data).native
	
	pprint(krbfastrep_dec)
	print('krbfastrep_dec sucsess dec')
	strengthen_key = Key(_enctype_table[krbfastrep_dec['strengthen-key']['keytype']].enctype , krbfastrep_dec['strengthen-key']['keyvalue'])
	computer_subkey = Key(_enctype_table[krbfastrep_dec['strengthen-key']['keytype']].enctype , computer_subkey_bytes)
	#dunno_key = cf2(krbfastrep_dec['strengthen-key']['keytype'], strengthen_key, computer_subkey, b"strengthenkey", b"replykey")


	cipherText = asrep['enc-part']['cipher']
	ku = None
	for i in range(100):
		try:
			armor_key = Key(_enctype_table[encfastrep['etype']].enctype, armor_key)
			tgt_encpart = _enctype_table[encfastrep['etype']].decrypt(strengthen_key, i, cipherText)
			tgt_encpart_dec = EncTGSRepPart.load(tgt_encpart).native
			ku = i
			pprint(tgt_encpart_dec)
			input()
		except:
			continue
	
	input(ku)
	

	return krbfastrep_dec['strengthen-key']['keyvalue'], krbfastrep_dec, armor_key


def decrypt_fast_tgs_req(session_key):
	print('==== decrypt_fast_tgs_req =====')
	tgs_req = bytes.fromhex('6c8206a6308206a2a103020105a20302010ca382061f3082061b30820520a103020101a2820517048205136e82050f3082050ba003020105a10302010ea20703050000000000a38204306182042c30820428a003020105a10b1b09544553542e434f5250a21e301ca003020102a11530131b066b72627467741b09544553542e434f5250a38203f2308203eea003020112a103020102a28203e0048203dce5f6db8e3c92a1f857ed0002a7ed9a30f85ef0aa9e08560e0128b17508ca36eda097ac98266da80129d578bd8af033b8378db62d256a50e665f0cdcf8175eb5fcf9a37fe101ecf816c6206595ac612b52680cf2a29aed78b68b56aae12c3367a79d5f3dd973d8cefb6ebc53ed9e1768ebb71e11f980ee75818bd86cdcd8213c1b12314b592429ea0975adc70cff2e871e12f60ecf8c1a05b95c280be491eb61bf5bab8603e9e60a8eafd16650deaac640a4f26de115d2837e1078a758129bc2d479c63534b44dfebbbdbfc8e5002017c46a1d1bd6066d7d28e902bb4b59800f9dcac9dd3a39d47d413daaf5f97e19ae125a9e547122b04abb7b05d4d72bafbd154c5407d7caa8d861e2ea64ee0fdcc8f1d777734f32cdad37898049bcc23c84968101738e887678238099d21ab14e10562d6c11933ff288394a4e3f501a078faff41eea0567262f304842796a913a6d3e4c845cd7f919da7702ea4077a71acac00778ce2994a10acc38bc9a1f88dc86f8646a08877af8708404d5bebf180986a9518d40e3f8bbffd324372617531f9a541b1f12c25fe680e29d5e6ea7cf4efca55848c9719f880099bfda9d8363db1847ad570cc9d110cce8fbd1073adea8a1d000482930c07e91e9e1791dc85caf267ea9a6dd69151ad8d542aca85ed3cb106eed8f173acddb7313b71a99f9cb490ec98cbd38e18504db29ae0f3b5d14602593730e9e5acacc49b892e7257dcf01cf68d08f921e9ae2c8ebbe790887a2038505f00f8fd9281581415096450a591af4f993b10f11dbf74598614e706664ba398b065f9263f0fd92e210575c647b3571147e207f3af51cd990a6bdfb501de55a15e6be55c63435bfc8336dfb367a7ea9b0673bfaafe9eeb67fd3e78aa5fd57f662449ce2be1032693504b3277da419a2dc20c28d3481bd4e2a02a3a23bfd690634cd596b22a34af1514c9a28ae8daa5757ad25a8d9f871ea5b9ea613171e1949f322045309877fa930cf5cb39c144e960b7e2a27d5a1dac8e7857c0cdc5548502b9352c0d3d71ba7a24a1fb3bc8dcf5786750abf8b57caeca7e9854e84c3fd85fe561c78568879191e29388d246185d4e9fd9e85907a71830bbe63a7270ad68523f940507ae322a7750c5f3aeda561b1bb3aed043557fc5023b1eba66db649753bb3099a9fde06be697c743a0954825c5ae4b3eab89ba86893365b65a9267f3b0c52a0198952512d12d044f47db039b0feba44f0d4cdc2c2aaab9dd86c568c73afa48d518e3e22b208d48d712554f11eedc5af8df587352d521dcb1c7bc52533f4752b477f922021777c014648853090202df6c7bcdd15329e83eb0688e0dafd0e7f4dcd5a5c27c9f2c1ea2d84d952a46c63398400b2d84ca322ea9b5a481c13081bea003020112a281b60481b39078e4333694f78ceb67fe2c88517ede8bf76d5964c5828d7a77a5d0de84fd75900c1e2c6577776bcb1e37b1b2186d639c6958070e7fc13b45a6459bc4f617ce97464b7349ddbb8ae80c52a94183e438b626044eb4da55b99e8733d6d21ca392417d062f65c0e3fa30107e310eec854209f3844d71ef24f4385dc408856fd70551ecc37d8f178c953dedfc44d97497140476d77e16686eb4473781c44b5a96c1f14aca3579403611b28975e2ff8d2cf8419ab93081f4a10402020088a281eb0481e8a081e53081e2a1173015a003020110a10e040ca2e51616ce6aa1c5ec5c2f30a281c63081c3a003020112a281bb0481b826fe13d8ae296cb05f282bcb50e04d7d01e8313344ef7eda9e126422e1ce61d129dea3277b7396af5f17312880584132d62c1cfab3582b378bfc2de4737a7d2a7e3a074b70d96ff4f4abfee40d38a5d90d64fe2f5ff2f9a9a6a6a25541d6fcfb639844c2f510b221f1768dc30e2140d3e57ddc4fb3da7f674fd718449eda6e42bc7fe5a5bd5790e7818447706522f6fe173234ec4533550e821acd6fe294575fb21002e597392931899902cb83a11006d5385edf6d84b4b8a4733071a00703050040810000a20b1b09544553542e434f5250a32a3028a003020103a121301f1b04686f73741b176f76657270726f7465637465642e746573742e636f7270a511180f32303337303931333032343830355aa706020461d06cb4a81230100201120201110201170201180202ff79')
	tgs_req_native = TGS_REQ.load(tgs_req).native
	pprint(tgs_req_native)


	# looking for the subkey, the subkey is in the authenticator of an AP_REQ which is in a PA-DATA element of type 1
	authenticator_enc_type = None
	authenticator_enc_data = None

	for padata in tgs_req_native['padata']:
		if padata['padata-type'] == 1:
			apreq = AP_REQ.load(padata['padata-value']).native
			authenticator_enc_type = apreq['authenticator']['etype']
			authenticator_enc_data = apreq['authenticator']['cipher']
			break
	
	a = None
	for i in range(100):
		try:
			decrypt_authenticator(authenticator_enc_type, authenticator_enc_data, session_key, key_usage = i)
			print(i)
			a = i
			break
		except Exception as e:
			print(e)
			continue

	if a is None:
		print('No key usage found :(')
	else:
		print('OK!!!!! %s' % a)

armor_key, decrypt_fast_as_req = decrypt_fast_as_req(computer_session_key_bytes)
strengthen_key, krbfastrep, armor_key = decrypt_fast_as_rep(armor_key, bytes.fromhex(cred.kerberos_key_aes_256))
print(strengthen_key)
decrypt_fast_tgs_req(armor_key.contents)

#salt = b'TEST.CORPhostoverprotected.test.corp'
#supp_enc = EncryptionType.AES256_CTS_HMAC_SHA1_96
#key_bytes = cred.get_key_for_enctype(supp_enc, salt)
#print('key_bytes %s' % key_bytes.hex())
#enc_data = asreq_2_native['padata'][0]['padata-value']
#decrypt_enctimestamp(enc_data, key_bytes, salt, supp_enc)