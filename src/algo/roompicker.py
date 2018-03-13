import random
import pandas as pd

class RoomPicker(object):

    def __init__(self, roommates, total_rent,old,old_list,turn):
        if old:
            self.roommates = roommates
            self.total_rent = total_rent
            self.turn = turn
            rooms_list = old_list
        else:
            self.roommates = roommates
            random.shuffle(self.roommates)
            self.total_rent = total_rent
            indiv_rent = total_rent / len(self.roommates)
            rooms_list = [[room_num + 1, roommate, indiv_rent] for room_num, roommate in enumerate(self.roommates)]
            self.turn = 0
        self.rooms_df = pd.DataFrame(rooms_list, columns=["room_number", "roommate", "rent"]).set_index("room_number")
        self.pass_count = 0

    def _get_room_number(self, roommate):
        return self.rooms_df[self.rooms_df["roommate"] == roommate].index.values[0]

    def _get_roommate(self, room_number):
        return self.rooms_df.loc[room_number, "roommate"]

    def _get_rent_from_roommate(self, roommate):
        return self.rooms_df[self.rooms_df["roommate"] == roommate].iloc[0, 1]

    def _get_rent_from_room_number(self, room_number):
        return self.rooms_df.loc[room_number, "rent"]

    def _set_roommate_and_rent(self, room_number, roommate, rent):
        self.rooms_df.loc[room_number] = [roommate, rent]

    def pass_dude(self):
        self.pass_count += 1
        self.turn += 1

    def run_algo(self, in_room_number, in_bid):
        print(in_bid)
        print(self.total_rent)
        if in_bid > self.total_rent:
            raise ValueError("Slow down Daddy Warbucks! Bid cannot be higher than total rent. Try again.")
        else:
            roommate = self.roommates[self.turn]
            old_room_number = self._get_room_number(roommate)
            if old_room_number == in_room_number:
                raise ValueError("Cannot choose room you already have! Try again.")
            elif in_room_number not in self.rooms_df.index.values:
                raise ValueError("Invalid room number! Try again.")
            else:
                current_rent = self._get_rent_from_room_number(in_room_number)
                if in_bid > current_rent:
                    current_roommate = self._get_roommate(in_room_number)
                    old_rent = self._get_rent_from_roommate(roommate)
                    self._set_roommate_and_rent(old_room_number, current_roommate, old_rent)
                    remaining_rent = self.total_rent - in_bid
                    rent_multiplier = remaining_rent / (self.total_rent - current_rent)
                    self.rooms_df["rent"] *= rent_multiplier
                    self._set_roommate_and_rent(in_room_number, roommate, in_bid)
                    self.rooms_df["rent"] = self.rooms_df["rent"].round()
                    if self.turn == len(self.roommates) - 1:
                        self.turn = 0
                    else:
                        self.turn += 1
                else:
                    raise ValueError("Bid must be higher than existing rent price! Try again.")
