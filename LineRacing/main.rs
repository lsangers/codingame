use std::io;

macro_rules! parse_input {
    ($x:expr, $t:ident) => ($x.trim().parse::<$t>().unwrap())
}
fn main() {

    const N: usize = 30;
    const M: usize = 20;

    let mut grid = [[0u8; N] ; M];


    let (nr_of_players,player_id, v) = read_input();

    println!("LEFT");
    // game loop
    loop {        

        // To debug: eprintln!("Debug message...");
        let (nr_of_players,player_id, v) = read_input();

        println!("LEFT"); 
    }
}

fn read_input() -> (u8, u8, Vec<u8>){
    let mut input_line = String::new();
    io::stdin().read_line(&mut input_line).unwrap();
    let inputs = input_line.split(" ").collect::<Vec<_>>();
    let nr_of_players = parse_input!(inputs[0], u8);
    let player_id = parse_input!(inputs[1], u8);
    let mut v: Vec<(u8,u8)> = Vec::new();
    for i in 0..nr_of_players as u8 {
        let mut input_line = String::new();
        io::stdin().read_line(&mut input_line).unwrap();
        v.extend(input_line.split(" ")
            .collect::<Vec<&str>>()
            .chunks(2)
            .map(|point| (parse_input!(point[0], u8), parse_input!(point[1], u8)))
            .chunks(2)
            .collect::<Vec<_>>());
    }

    return (nr_of_players,player_id, v)
}