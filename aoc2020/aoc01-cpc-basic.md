# HOWTO CPC

## Caprice Forever: Amstrad CPC emulator for Windows (includes Sorcery disk)

<https://www.cpc-power.com/cpcarchives/index.php?page=articles&num=73>

## ARNOLD: Amstrad CPC emulator for Max and Windows

<https://www.cpcwiki.eu/index.php/Arnold_(Emulator)>

## IDSK: to deal with "floppy disks"

<http://koaks.amstrad.free.fr/amstrad/projets/>

download source as tgz and compile with make

Create floppy disk container:

```txt
./iDSK -n aoc2020.dsk
./iDSK aoc2020.dsk -n aoc2020.dsk
```

Copy text file into "floppy disk"

```txt
./iDSK aoc2020.dsk -i ~/Desktop/aoc-01.txt -t 0
```

See list of files that are in this disk

```txt
./iDSK aoc2020.dsk -l
```

Extract file from disk

```txt
./iDSK aoc2020.dsk -b AOC01.BAS > AOC01.BAS
./iDSK aoc2020.dsk -b AOC01-2.BAS > AOC01-2.BAS
```

## CPC Emulator in Browser - with games

<https://www.retrovm.com/>
