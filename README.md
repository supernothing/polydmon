# polydmon
watch polyswarm go

## install

```
python setup.py install
```

## usage

```
$ polydmon --help
Usage: polydmon [OPTIONS]

Options:
  --event [bounty|assertion|vote|all]
  --uri [wss://nu.k.polyswarm.network/v1/events/?chain=side|wss://lima.polyswarm.network/events?chain=side|all]
  --json
  --help                          Show this message and exit.
```

```
$ polydmon                                                                                                                                                                                                                           
event: connected, block_number:                                                                                                                                                                                                                                                
event: connected, block_number:                                                                                                                                                                                                                                                
event: assertion, block_number: 1588022492, author: 0x1EdF29c0977aF06215032383F93deB9899D90118, bid: 812500000000000000, extended_type: , bounty_guid: 8d5c791b-8ca1-40fe-8c51-00b361f6a4e8
event: assertion, block_number: 1588022492, author: 0xa328255e92f2284251d29C41Eb6D0947a49eF338, bid: 1000000000000000000, extended_type: , bounty_guid: d8792160-2160-4b3c-bb83-828b3644a0d6
event: assertion, block_number: 1588022492, author: 0xa328255e92f2284251d29C41Eb6D0947a49eF338, bid: 1000000000000000000, extended_type: , bounty_guid: 59a4175c-e7c2-4412-8372-38cbd3b74a3e
event: assertion, block_number: 1588022492, author: 0xa328255e92f2284251d29C41Eb6D0947a49eF338, bid: 953125000000000000, extended_type: , bounty_guid: ba052a96-4e42-40ac-be38-bc267b3ff1ba
event: assertion, block_number: 1588022492, author: 0x2b4C240B376E5406C5e2559C27789d776AE97EFD, bid: 1000000000000000000, extended_type: , bounty_guid: c752c961-cd35-4c2a-b609-a7d3edfed432
event: assertion, block_number: 1588022492, author: 0xa328255e92f2284251d29C41Eb6D0947a49eF338, bid: 1000000000000000000, extended_type: , bounty_guid: 1cb36aed-8885-49b7-a7d2-fabc51f4365d
event: vote, block_number: 1588022492, voter: 0xdC6a0F9C3AF726Ba05AaC14605Ac9B3b958512d7, votes: True, bounty_guid: 8aa7e5fc-32ba-4cad-9c15-9ddf97c6f318
event: vote, block_number: 1588022492, voter: 0xdC6a0F9C3AF726Ba05AaC14605Ac9B3b958512d7, votes: True, bounty_guid: fc18c35b-f4c8-45c6-9e7e-4fdf5c70733e
event: vote, block_number: 1588022492, voter: 0xdC6a0F9C3AF726Ba05AaC14605Ac9B3b958512d7, votes: False, bounty_guid: e7728917-3463-456e-99bf-017765321052
event: vote, block_number: 1588022492, voter: 0xdC6a0F9C3AF726Ba05AaC14605Ac9B3b958512d7, votes: True, bounty_guid: 380aa210-54fd-462c-a165-3df213c45c6a
event: vote, block_number: 1588022492, voter: 0xdC6a0F9C3AF726Ba05AaC14605Ac9B3b958512d7, votes: False, bounty_guid: 997d98e6-3fa0-479e-855c-27471716910d
event: vote, block_number: 1588022492, voter: 0xdC6a0F9C3AF726Ba05AaC14605Ac9B3b958512d7, votes: True, bounty_guid: 8625e26a-7599-4890-85c8-ff344cf0a3e0
event: vote, block_number: 1588022492, voter: 0xdC6a0F9C3AF726Ba05AaC14605Ac9B3b958512d7, votes: False, bounty_guid: 09990811-afd5-48b7-aa18-daeab713e035
event: vote, block_number: 1588022492, voter: 0xdC6a0F9C3AF726Ba05AaC14605Ac9B3b958512d7, votes: False, bounty_guid: 5e33748f-8435-4b9c-8b9e-6a586eae262a
event: vote, block_number: 1588022492, voter: 0xdC6a0F9C3AF726Ba05AaC14605Ac9B3b958512d7, votes: True, bounty_guid: 2a5d25c8-2264-48d3-8071-933d31dca157
event: vote, block_number: 1588022492, voter: 0xdC6a0F9C3AF726Ba05AaC14605Ac9B3b958512d7, votes: True, bounty_guid: eaf4581b-3a53-4feb-82fb-64ffdd6c48a9
event: assertion, block_number: 1588022492, author: 0xa328255e92f2284251d29C41Eb6D0947a49eF338, bid: 1000000000000000000, extended_type: , bounty_guid: 28b00ea2-636f-48ea-80dc-53b8bcc39d02
event: assertion, block_number: 1588022492, author: 0xa328255e92f2284251d29C41Eb6D0947a49eF338, bid: 953125000000000000, extended_type: , bounty_guid: c0814e7e-a404-4060-9b6b-1ba1a9212d01
event: assertion, block_number: 1588022492, author: 0x162675F361F6ff8D6F91e4833f4BA94587AF3655, bid: 1000000000000000000, extended_type: , bounty_guid: d8792160-2160-4b3c-bb83-828b3644a0d6
```
