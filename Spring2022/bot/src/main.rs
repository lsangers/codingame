use std::io;

macro_rules! parse_input {
    ($x:expr, $t:ident) => ($x.trim().parse::<$t>().unwrap())
}

#[derive(PartialEq)]
enum Player{
    Me,
    Enemy,
}

#[derive(PartialEq)]
enum Type {
    Monster,
    Hero(Player),
}

impl Type{
    fn from_u16(t: u16) -> Self{
        match t {
            1_u16 => Type::Hero(Player::Me),
            2_u16 => Type::Hero(Player::Enemy),
            _ => Type::Monster,
        }
    }
}

#[derive(PartialEq)]

enum Threat{
    None,
    Base(Player),
}

impl Threat{
    fn from_u16(t: u16) -> Self{
        match t {
            1_u16 => Threat::Base(Player::Me),
            2_u16 => Threat::Base(Player::Enemy),
            _ => Threat::None,
        }
    }
}

#[derive(PartialEq)]
enum Action{
    Moving,
    Targetting,
}

impl Action{
    fn from_u16(t: u16) -> Self{
        match t {
            1_u16 => Action::Targetting,
            _ => Action::Moving,
        }
    }
}

struct Base{
    x: u16,
    y: u16,
    health: u16,
    mana: u16,
}

impl Base {
    pub fn other(&self) -> Self {
        Self {
            x: 1,
            y: 1,
            health: self.health,
            mana: self.health,
        }
    }
}

struct Entity{
    id: u16,
    x: u16,
    y: u16,
    r#type: Type,
    shield_life: u16,
    is_controlled: u16,
    health: u16,
    vx: i16,
    vy: i16,
    action: Action,
    threat_for: Threat,
}

impl Entity{
    pub fn new(inputs: Vec<&str>) -> Self{
        Entity {
            id: parse_input!(inputs[0], u16), // Unique identifier
            r#type: Type::from_u16(parse_input!(inputs[1], u16)), // 0=monster, 1=your hero, 2=opponent hero
            x: parse_input!(inputs[2], u16), // Position of this entity
            y: parse_input!(inputs[3], u16),
            shield_life: parse_input!(inputs[4], u16), // Ignore for this league; Count down until shield spell fades
            is_controlled: parse_input!(inputs[5], u16), // Ignore for this league; Equals 1 when this entity is under a control spell
            health: parse_input!(inputs[6], u16), // Remaining health of this monster
            vx: parse_input!(inputs[7], i16), // Trajectory of this monster
            vy: parse_input!(inputs[8], i16),
            action: Action::from_u16(parse_input!(inputs[9], u16)), // 0=monster with no target yet, 1=monster targeting a base
            threat_for: Threat::from_u16(parse_input!(inputs[10], u16)), // Given this monster's trajectory, is it a threat to 1=your base, 2=your opponent's base, 0=neither
        }
    }
}

fn main() {
    let mut input_line = String::new();
    io::stdin().read_line(&mut input_line).unwrap();
    let inputs = input_line.split(' ').collect::<Vec<_>>();

    let mut my_base = Base {
        x: parse_input!(inputs[0], u16),
        y: parse_input!(inputs[1], u16),
        health: 0,
        mana: 0,
    };

    let mut enemy_base = my_base.other();

    let mut input_line = String::new();
    io::stdin().read_line(&mut input_line).unwrap();
    let heroes_per_player = parse_input!(input_line, u16); // Always 3

    // game loop
    loop {
        let mut input_line = String::new();
        io::stdin().read_line(&mut input_line).unwrap();
        let inputs = input_line.split(' ').collect::<Vec<_>>();
        my_base.health = parse_input!(inputs[0], u16);
        my_base.mana = parse_input!(inputs[1], u16);
        
        let mut input_line = String::new();
        io::stdin().read_line(&mut input_line).unwrap();
        let inputs = input_line.split(' ').collect::<Vec<_>>();
        enemy_base.health = parse_input!(inputs[0], u16);
        enemy_base.mana = parse_input!(inputs[1], u16);


        let mut input_line = String::new();
        io::stdin().read_line(&mut input_line).unwrap();
        let entity_count = parse_input!(input_line, u16); // Amount of heros and monsters you can see
        let mut entities: Vec<Entity> = Vec::new();
        for _ in 0..entity_count {
            let mut input_line = String::new();
            io::stdin().read_line(&mut input_line).unwrap();
            let inputs = input_line.split(' ').collect::<Vec<_>>();
            entities.push(Entity::new(inputs));
        }

        let my_heros = entities.iter().filter(|&entity| entity.r#type == Type::Hero(Player::Me)).collect::<Vec<&Entity>>();
        
        let attacking_enemies = entities.iter().filter(|&entity| entity.threat_for == Threat::Base(Player::Me)).collect::<Vec<&Entity>>();
        for hero in my_heros {

            // Write an action using println!("message...");
            // To debug: eprintln!("Debug message...");


            // In the first league: MOVE <x> <y> | WAIT; In later leagues: | SPELL <spellParams>;
            println!("WAIT");
        }
    }
}
