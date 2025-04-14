# Resources Pack Compiler

This is a simple tool to compile a resource pack for Minecraft.
Very useful for server owners who want to create a custom resource pack for their server as server.properties only allows one required ressource pack.

## Usage

1. Clone the repository
```shell
git clone https://github.com/Hugo-CASTELL/resources-pack-compiler.git && cd resources-pack-compiler
```
2. Create a `ressources` folder in the root of the repository
```shell
mkdir ressources
```
3. Download the resource packs you want to compile and put them in the `ressources` folder
4. Each resource pack **must be a .zip file** and have to be **numerate in order followed by an underscore** as the example below.
```txt
ressources/1_pack.zip (order them in the same order you would do in your minecraft options)
ressources/2_pack.zip (1 being the pack at the top of the list, 2 the second, etc...)
ressources/3_pack.zip
ressources/4_pack.zip
ressources/5_pack.zip
ressources/6_pack.zip
ressources/6_pack2.zip (ignored, no duplicate order number)
ressources/7_pack.zip 
ressources/10_pack.zip (they don't have to be consecutive)
```
5. Run the script
```shell
python3 compiler.py
```