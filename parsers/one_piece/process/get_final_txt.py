from parsers.functions.convert import by_hand_txt_to_final_data_txt

by_hand_txt_to_final_data_txt('../data/filtered_by_hand.txt', final_path='../data/one_piece.txt',
                              columns_to_drop=[0, 3])
