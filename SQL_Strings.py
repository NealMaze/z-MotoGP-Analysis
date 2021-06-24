

dropTimesTable = """
    DROP TABLE gp_times
    """

createTimesTable = """
    CREATE TABLE gp_times(
    
        index text PRIMARY KEY,
        month text,
        day text,
        yr integer,
        lge text,
        rnd integer,
        session text,
        trk text,
        
        pos text,
        rdr_num integer,
        f_name text,
        l_name text,
        nat text,
        team text,
        manu text,
        num_of_laps integer,
        
        run_num integer,
        f_tire text,
        r_tire text,
        laps_on_f integer,
        laps_or_r integer,
        lap_num integer,
        
        lap_time text,
        lap_seconds decimal,
        lap_valid boolean,
        
        pit boolean,
        
        sec_one text,
        one_seconds decimal,
        one_valid boolean,
        
        sec_two text,
        two_seconds decimal,
        two_valid boolean,
        
        sec_thr text,
        thr_seconds decimal,
        thr_valid boolean,
        
        sec_four text,
        four_seconds decimal,
        four_valid boolean,
        
        avg_spd text
        )
    """