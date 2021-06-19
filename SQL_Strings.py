



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
        pit text,
        sec_one text,
        sec_two text,
        sec_thr text,
        sec_four text,
        sec_fiv text,
        sec_six text,
        sec_sev text,
        sec_eig text,
        avg_spd text
        )
    """