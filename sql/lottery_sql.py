INSERT_MEGA645 = '''
INSERT IGNORE INTO lottery.mega645
(id, numbers, draw_date, created_by, created_time, updated_time)
VALUES(%s, %s, %s, %s, current_timestamp(), current_timestamp());
'''