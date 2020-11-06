import json
import os

class Database():
    
    def __init__(self):
        self.users = {} # k: "username" v: user object
        self.songs = {}
        self.playlists = {}
        self.queue = []
        self.active_user = None
        self.active_song = None
        self.run = True
        
        
    # Sets the current active user
    def login(self):
        username = input("Enter your user name: ")
        password = input("Enter your password: ")

        if username in self.users:
            if password == self.users[username].password:
                self.active_user = self.users[username]
                return True
            else:
                print("Error: Incorrect password!")
                return False
        else:
            print("Error: No user found!")
            return False

    
    def delete_user(self):
        response = input("Are you sure you want to delete your account? y/n")
        if response == "y":
            self.users.pop(self.active_user.name)
            self.active_user = None
        
    # create user is taken care of in User

    def delete_playlist(self):
        playlist = input("Enter name of playlist to be deleted: ")

        if playlist in self.playlists:
            self.playlists.pop[playlist]
        else:
            print("Playlist not found") 
    
    def play(self):
        self.active_song = self.queue[0]
        print(f"Playing Song: {self.active_song.name}.")

    def pause(self):
        print("Paused Song.")

    def skip(self):
        self.queue.pop(0)
        self.active_song = self.queue[0]
        print("Skipped Song.")
        
    def browse_content(self):
        
        # While loop can probs go here
        while(self.active_user != None):
            print("1. Upload Song\n"
                    "2. Create Playlist\n"
                    "3. List All Songs\n"
                    "4. List All Artists\n"
                    "5. List All Albums\n"
                    "6. Playlist Menu\n"
                    "7. Delete Your Account\n"
                    "8. Sign Out")

            option = int(input("..."))
            if(option == 1):
                song1 = Song.create_song()
                self.songs[song1.name] = song1
                
            elif(option == 2):
                playlist1 = Playlist.create_playlist()
                self.playlists[playlist1.name] = playlist1

            elif(option == 3):
                for song in self.songs.values():
                    print(song.name)

            elif(option == 4):
                for song in self.songs.values():
                    print(song.artist)
            
            elif(option == 5):
                for song in self.songs.values():
                    print(song.album)

            elif(option == 6):
                self.playlist_menu()
            
            elif(option == 7):
                self.delete_user()
            
            elif(option == 8):
                self.active_user = None
            else:
                print("Error: not a valid option!")


    def playlist_menu(self):

        print(
            "1. Add songs to playlist\n"
            "2. Remove songs from playlist\n"
            "3. Reorder songs in playlist\n"
            "4. Delete playlist\n"
            "5. Go back to menu"
        )
        
        option = int(input("..."))
        
        if(option == 1):
            playlist = input("Which playlist do you want to edit?")
            if playlist in self.playlists:

                current_playlist = self.playlists[playlist]
                
                name_of_song = input("What song do you want to add?")
                song_to_add = self.songs[name_of_song]
                current_playlist.add_song(song_to_add)
            else:
                print("Error: Playlist Not Found!")
                
        elif(option == 2):
            playlist = input("Which playlist do you want to edit?")
            if playlist in self.playlists:

                current_playlist = self.playlists[playlist]
                
                for i in range(len(current_playlist.songs)):
                    print(str(i) + " " + current_playlist.songs[i].name)

                song_number = int(input("What song number do you want to remove?"))
                current_playlist.remove_song(song_number)
            else:
                print("Error: playlist not found!")

        elif(option == 3):
            playlist = input("Which playlist do you want to edit?")
            if playlist in self.playlists:
                current_playlist = self.playlists[playlist] 
                
                for i in range(len(current_playlist.songs)):
                    print(str(i) + " " + current_playlist.songs[i].name)     

                swap_first = int(input("Which number song do you want to move?"))
                swap_second = int(input("Which number song do you want to move it with?"))

                current_playlist.swap_songs(swap_first, swap_second)
            else:
                print("Error: playlist not found!")

        elif(option == 4):    
            playlist = input("What playlist do you want to delete?")
            if playlist in self.playlists:
                self.playlists.pop(playlist)
            else:
                print("Error: Playlist not found!")

        
        
        elif(option == 5):
            pass


    def main_menu(self):

        print(
        "1. Create Account\n"
        "2. Login\n"
        "3. Quit\n"
        )
        
        optionChoosen = int(input("..."))

        if (optionChoosen == 1):
            # Something missing
            temp = User.create_user()
            self.users[temp.name] = temp

        elif(optionChoosen == 2):
            if(self.login()):
                self.browse_content()

        elif(optionChoosen == 3):
            self.run = False


    def load(self):
        with open("data/users.json","r") as user_file:
            user_dictionary = json.load(user_file)
            for dictionary in user_dictionary:
                temp = User.from_dict(dictionary)
                self.users[temp.name] = temp

        with open("data/songs.json", "r") as song_file:
            song_dictionary = json.load(song_file)
            for dictionary in song_dictionary:
                temp = Song.from_dict(dictionary)
                self.songs[temp.name] = temp


        with open("data/playlists.json", "r") as playlist_file:
            playlist_dictionary = json.load(playlist_file)
            for dictionary in playlist_dictionary:
                temp = Playlist.from_dict(dictionary)
                self.playlists[temp.name] = temp

    def save(self):
        with open("data/users.json","w") as user_file:
            user_data = []
            for user in self.users.values():
                data = user.to_dict()
                user_data.append(data)
            json.dump(user_data, user_file)
                
        
        with open("data/songs.json", "w") as song_file:
            song_data = []
            for song in self.songs.values():
                data = song.to_dict()
                song_data.append(data)
            json.dump(song_data, song_file)

        with open("data/playlists.json", "w") as playlist_file:
            playlist_data = []
            for playlist in self.playlists.values():
                data = playlist.to_dict()
                playlist_data.append(data)
            json.dump(playlist_data, playlist_file)


class User():
    
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def to_dict(self):
        return {
            "name" : self.name,
            "email" : self.email,
            "password" : self.password
        }

    @staticmethod
    def from_dict(dictionary):
        name = dictionary["name"]
        email = dictionary["email"]
        password = dictionary["password"]
        return User(name, email, password)
    
    @staticmethod
    def create_user():
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        return User(name, email, password)


class Song():

    def __init__(self, name, artist, album):
        self.name = name
        self.artist = artist
        self.album = album
    
    @staticmethod
    def create_song():
        name = input("Enter song name: ")
        artist = input("Enter song artist: ")
        album = input("Enter album: ")
        return Song(name, artist, album)    
    

    def to_dict(self):
        return {
            "name" : self.name,
            "artist" : self.artist,
            "album" : self.album
        }
        
    @staticmethod
    def from_dict(dict):
        name = dict["name"]
        artist = dict["artist"]
        album = dict["album"]
        return Song(name, artist, album)


class Playlist():

    def __init__(self, playlist_name, songs):
        self.name = playlist_name
        self.songs = songs
        self.owner = None
    
    def add_song(self, song):
        self.songs.append(song)
        
    def create_playlist():
        name = input("Enter the playlist name: ")
        return Playlist(name, [])
    
    def remove_song(self, song):
        self.songs.pop(song)

    # need to decide arguments, static/object, and how it works
    
    def swap_songs(self, position1, position2):
        
        temp = self.songs[position1]

        self.songs[position1] = self.songs[position2]
        self.songs[position2] = temp

    def to_dict(self):
        return {
            "name" : self.name,
            "songs": [song.to_dict() for song in self.songs],
        }
    @staticmethod
    def from_dict(dictionary):
        name = dictionary["name"]
        songs = [Song.from_dict(child) for child in dictionary["songs"]]
        return Playlist(name, songs)

if __name__ == "__main__":

    database1 = Database()

    database1.load()

    while(database1.run):
        database1.main_menu()

    database1.save()