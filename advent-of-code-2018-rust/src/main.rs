use std::fs;
use std::collections::HashMap;
use std::collections::HashSet;
use std::collections::BTreeMap;
use std::ops::Range;

#[derive(PartialEq, Eq, Hash, Clone, Copy, Ord, PartialOrd)]
struct Point {
    x: i32,
    y: i32,
}



impl Point {
    fn neighbours(&self) -> Vec<Point> {
        let mut vec =  Vec::new();
        vec.push(Point {x: self.x-1, y: self.y-1});
        vec.push(Point {x: self.x, y: self.y-1});
        vec.push(Point {x: self.x+1, y: self.y-1});
        vec.push(Point {x: self.x-1, y: self.y});
        vec.push(Point {x: self.x+1, y: self.y});
        vec.push(Point {x: self.x-1, y: self.y+1});
        vec.push(Point {x: self.x, y: self.y+1});
        vec.push(Point {x: self.x+1, y: self.y+1});
        return vec;
    }
}

fn main() {

    let contents = fs::read_to_string("input/day18.dat").expect("Could not read file");

    let char_vec: Vec<char> = contents.chars().collect();

    let mut acres = BTreeMap::new();


    let mut row = 0;
    let mut column = 0;
    let mut calculated_width = 0;
    let mut calculated_height = 0;
    for c in char_vec {
        if c == '\n' {
            row += 1;
            column = 0;
            calculated_height = if calculated_height < row { row } else {calculated_height};
        } else {
            acres.insert(Point {x: column, y: row}, c);
            calculated_width = if calculated_width < column { column } else {calculated_width};
            column += 1;
        }
    }

    println!("height {}", calculated_height);
    println!("width {}", calculated_width);
    println!("{}", acres.len());

    print_acres(&acres, calculated_width, calculated_height);
    
    //for _i in (Range {start:0, end: 10}) {
    let mut previousAcres = HashSet::new();
    let mut firstRepeat = 0;
    loop {
        let asd = previousAcres.contains(&acres);
        //println!("{}", asd);
        if asd {
            // this acre is the first repeated instance, but how long is the loop?
            println!("Loop starts at {}", firstRepeat);
            break;
        }
        previousAcres.insert(acres.clone());
        acres = advance(&acres, calculated_width, calculated_height);
        // println!("");
        // print_acres(&acres, calculated_width, calculated_height);
        // println!("");
        firstRepeat += 1;
    }

    
    previousAcres = HashSet::new();
    let mut loopCount = 0;
    loop {
        if previousAcres.contains(&acres) {
            // this acre is the first repeated instance, but how long is the loop?
            println!("Loop is {} long", loopCount);
            break;
        }
        previousAcres.insert(acres.clone());
        acres = advance(&acres, calculated_width, calculated_height);
        loopCount += 1;
    }

    let iterations_to_compute = 1000000000;
    let loopsLeft = (1000000000 - firstRepeat) % loopCount;

    for i in (Range{start: 0, end: loopsLeft}) {
        acres = advance(&acres, calculated_width, calculated_height);
    }

    println!("");
    print_acres(&acres, calculated_width, calculated_height);

    let mut resource_frequency = FrequencyAnalyser::new();
    for y1 in (Range {start: 0, end: calculated_height+1}) {
        for x1 in (Range {start: 0, end: calculated_width+1}) {
            match acres.get(&Point{x: x1, y: y1}) {
                Some(c) => resource_frequency.add(*c),
                None => ()
            }
        } 
    }
    println!("|: {}, #: {}, {}", resource_frequency.how_many('|'), resource_frequency.how_many('#'), resource_frequency.how_many('|') * resource_frequency.how_many('#'));
    
}

fn print_acres(acres: &BTreeMap<Point, char>, calculated_width: i32, calculated_height: i32) {
    for y1 in (Range {start: 0, end: calculated_height+1}) {
        for x1 in (Range {start: 0, end: calculated_width+1}) {
            match acres.get(&Point{x: x1, y: y1}) {
                Some(c) => print!("{}", c),
                None => print!("-")
            }
        } 
        println!("")
    }
}

fn advance(acres: &BTreeMap<Point, char>, calculated_width: i32, calculated_height: i32) -> BTreeMap<Point, char> {
    let mut new_acres = BTreeMap::new();
    for y1 in (Range {start: 0, end: calculated_height+1}) {
        for x1 in (Range {start: 0, end: calculated_width+1}) {
            let current_point = Point{x: x1, y: y1};
            match acres.get(&current_point) {
                Some(c) => new_acres.insert(current_point, cell_advance(c, current_point, acres)),
                None => None,
            };
        } 
    }
    return new_acres;
}

fn cell_advance(current_acre: &char, current_point: Point, acres: &BTreeMap<Point, char>) -> char {
    let neighbours = current_point.neighbours();
    let mut neighbour_freq = FrequencyAnalyser::new();
    for n in neighbours {
        match acres.get(&n) {
            Some(c) => neighbour_freq.add(*c),
            None => ()
        }
    }
    //let Point {x, y} = current_point;
    //println!("count . {} at Pos ({},{})", freq.how_many('.'), x, y);
    if *current_acre == '.' {
        return if neighbour_freq.how_many('|') >= 3 {'|'} else { '.' }
    } else if *current_acre == '|' {
        return if neighbour_freq.how_many('#') >= 3 {'#'} else { '|' }
    } else if *current_acre == '#' {
        return if neighbour_freq.how_many('#') >= 1 && neighbour_freq.how_many('|') >= 1 {'#'} else { '.' }
    }
    return 'c';
}

struct FrequencyAnalyser {
    frequency_counter: HashMap<char, i32>,
}

impl FrequencyAnalyser {
    fn new() -> FrequencyAnalyser {
        return FrequencyAnalyser{frequency_counter: HashMap::new()}
    }

    fn add(&mut self, c: char) {
        match self.frequency_counter.get(&c) {
            Some(count) => self.frequency_counter.insert(c, count+1),
            None => self.frequency_counter.insert(c, 1)
        };
    }

    fn how_many(&self, c: char) -> i32 {
        return match self.frequency_counter.get(&c) {
            Some(count) => *count,
            None => 0
        };
    }
}