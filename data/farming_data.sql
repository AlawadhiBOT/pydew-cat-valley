CREATE TABLE farmableData (
    i INTEGER NOT NULL,
    j INTEGER NOT NULL,
    farmable BOOL NOT NULL,
    PRIMARY KEY (i, j)
);

CREATE TABLE plantedData (
    i INTEGER NOT NULL,
    j INTEGER NOT NULL,
    PRIMARY KEY (i, j),
    FOREIGN KEY (i, j) REFERENCES farmData(i, j)
);

CREATE TABLE plantData (
    plant_type  CHAR(50) NOT NULL,
    age         INTEGER NOT NULL,
    left        INTEGER NOT NULL,
    top         INTEGER NOT NULL,
    PRIMARY KEY (left, top)
);