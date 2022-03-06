# X-Forward-By
Works on direct forwarding preserving the sender signature in an SMTP exchange


## Platform deployment

To validate the ability of SMTP servers to deal with the *X-Forward-By* field, and do our tests we build a virtualized platform using VirtualBox.

The whole platform installation and deployment is described [here](SimplePostfixArchitecture.md) (file in french).


## Thunderbird development works

### Extensions
To test the SMTP headers interpretation and confirm it was exploitable, we develop the 2 extensions below:
- ThunderBird Extension [message infos](TDB_Extension/messageInfos/) accesses the SMTP headers of the message, precising the `x-forward-by` content.  
- ThunderBird Extension [Forward Signed](TDB_Extension/TBE_ForwardSigned/) allows the forwarding of the message using the `x-forward-by` SMTP field that preserves the signature (development in progress).

> The installation of extensions in Thunderbird is described in [here](SimplePostfixArchitecture.md#Test) at paragraph `Installation extension TDB`.


