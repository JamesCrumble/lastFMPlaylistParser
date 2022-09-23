from general import get_compositions

if __name__ == '__main__':
    print('#'*50 + '\nCREATED BY "James_Crumble aka namster222333"\n' + '#'*50 + '\n')

    if compositions := get_compositions():

        # Actually last played or listening now composition is first element of the list
        latest_composition = compositions[0]
        print(f'\nFOUND "{len(compositions)}" LAST PLAYED COMPOSITIONS\n')
        print(
            f'POSSIBLE LATEST PLAYED OR CURRENTY LISTENING COMPOSITION: \n'
            f'\tNAME: {latest_composition.name}\n'
            f'\tARTIST: {latest_composition.artist}\n'
            f'\tLAST PLAYED: {latest_composition.last_played}\n'
            f'\tLISTENING_NOW: {latest_composition.listening_now}'
        )
