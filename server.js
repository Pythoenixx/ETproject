import express from 'express';
import mysql from 'mysql2/promise';
import cors from 'cors';

const app = express();
app.use(cors());
app.use(express.json());

// MySQL Connection
const db = await mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '',
  database: 'forest'
});

// Test endpoint
app.get('/', (req, res) => {
  res.send('Backend is running');
});

// Forest trees endpoint
app.get('/api/forest-trees', async (req, res) => {
  try {
    const [results] = await db.query(`
      SELECT 
        treeNum,
        species,
        block_x,
        block_y,
        coord_x,
        coord_y,
        diameter_cm,
        height_m,
        volume_m3,
        species_group
      FROM forest_trees
    `);
    res.json(results);
  } catch (err) {
    console.error('Database error:', err);
    res.status(500).json({ error: 'Database query failed' });
  }
});

app.get('/api/final_output/:regime', async (req, res) => {
  const regime = req.params.regime;
  const validRegimes = ['45', '50', '55', '60', '65'];
  
  if (!validRegimes.includes(regime)) {
    return res.status(400).json({ error: 'Invalid regime specified' });
  }

  try {
    const tableName = `final_output${regime}`;
    const [results] = await db.query(`SELECT * FROM ${tableName}`);
    res.json(results);
  } catch (err) {
    console.error(`Error fetching final output for regime ${regime}:`, err);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// Optional default route for backward compatibility
app.get('/api/final_output', async (req, res) => {
  req.params = { regime: '45' };
  return app._router.handle(req, res);
});

// Forest data endpoint
app.get('/api/forest-data', async (req, res) => {
  try {
    const allowedTables = ['forest_45', 'forest_50', 'forest_55', 'forest_60', 'forest_65'];

    const table = req.query.table;

    // Validate the table
    if (!allowedTables.includes(table)) {
      return res.status(400).json({ error: 'Invalid table name' });
    }

    let query = `
      SELECT 
        BlockX, BlockY, x, y, TreeNum, species, spgroup, 
        Diameter as diameter, 
        \`Stem Height\` as height, 
        Volume as volume,
        status, PROD, 
        \`Damage CutAngle\` as cut_angle,
        \`Damage STEM\` as stem_damage,
        \`Damage Crown\` as crown_damage,
        d30, VOL30
      FROM ${table}
    `;

    const params = [];
    const { species, minDiameter, status, damageLevel } = req.query;
    const whereClauses = [];

    if (species) {
      whereClauses.push('species LIKE ?');
      params.push(`%${species}%`);
    }

    if (minDiameter) {
      whereClauses.push('Diameter >= ?');
      params.push(parseFloat(minDiameter));
    }

    if (status) {
      whereClauses.push('status = ?');
      params.push(status);
    }

    if (damageLevel) {
      if (damageLevel === 'none') {
        whereClauses.push('(`Damage STEM` IS NULL OR \`Damage STEM\` = "")');
        whereClauses.push('(`Damage Crown` IS NULL OR \`Damage Crown\` = "")');
      } else {
        whereClauses.push('(`Damage STEM` LIKE ? OR \`Damage Crown\` LIKE ?)');
        params.push(`%${damageLevel}%`);
        params.push(`%${damageLevel}%`);
      }
    }

    if (whereClauses.length > 0) {
      query += ' WHERE ' + whereClauses.join(' AND ');
    }

    const validColumns = [
      'BlockX', 'BlockY', 'TreeNum', 'species', 'spgroup', 'diameter',
      'height', 'volume', 'status', 'PROD', 'cut_angle',
      'stem_damage', 'crown_damage', 'd30', 'VOL30'
    ];

    if (req.query.sortBy && validColumns.includes(req.query.sortBy)) {
      query += ` ORDER BY ${req.query.sortBy}`;
      if (req.query.sortDir === 'desc') {
        query += ' DESC';
      }
    }

    if (req.query.limit) {
      query += ' LIMIT ?';
      params.push(parseInt(req.query.limit));
      if (req.query.offset) {
        query += ' OFFSET ?';
        params.push(parseInt(req.query.offset));
      }
    } else {
    }

    const [rows] = await db.query(query, params);
    res.json(rows);
  } catch (error) {
    console.error('Error fetching forest data:', error);
    res.status(500).json({ 
      error: 'Failed to fetch forest data',
      details: error.message 
    });
  }
});

// API route to fetch stand table data by regime
app.get('/api/stand-table', async (req, res) => {
  const regime = req.query.regime;

  if (!regime) {
    return res.status(400).json({ error: 'Missing regime parameter' });
  }

  const validRegimes = ['45', '50', '55', '60', '65'];
  if (!validRegimes.includes(regime)) {
    return res.status(400).json({ error: 'Invalid regime value' });
  }

  const tableName = `stand_table_${regime}`;

  try {
    const [results] = await db.query('SELECT * FROM ??', [tableName]);
    res.json(results);
  } catch (err) {
    console.error('Database query error:', err);
    res.status(500).json({ error: 'Database query failed' });
  }
});

// Stand Table Damage by Regime
app.get('/api/stand-table-damage', async (req, res) => {
  const regime = req.query.regime;

  // Validate regime
  if (!regime || !['45', '50', '55', '60', '65'].includes(regime)) {
    return res.status(400).json({ error: 'Invalid or missing regime parameter' });
  }

  const tableName = `stand_table_damage${regime}`;

  try {
    const [results] = await db.query(`SELECT * FROM ??`, [tableName]);
    res.json(results);
  } catch (error) {
    console.error('Error fetching stand_table_damage:', error);
    res.status(500).json({ error: 'Failed to fetch stand table damage data' });
  }
});

// Stand Table Production by Regime
app.get('/api/stand-table-production', async (req, res) => {
  const regime = req.query.regime;

  // Validate regime
  if (!regime || !['45', '50', '55', '60', '65'].includes(regime)) {
    return res.status(400).json({ error: 'Invalid or missing regime parameter' });
  }

  const tableName = `stand_table_production${regime}`;

  try {
    const [results] = await db.query(`SELECT * FROM ??`, [tableName]);
    res.json(results);
  } catch (error) {
    console.error('Error fetching stand_table_production:', error);
    res.status(500).json({ error: 'Failed to fetch stand table production data' });
  }
});

// Stand Table Production by Regime
app.get('/api/stand-table-remaining', async (req, res) => {
  const regime = req.query.regime;

  // Validate regime
  if (!regime || !['45', '50', '55', '60', '65'].includes(regime)) {
    return res.status(400).json({ error: 'Invalid or missing regime parameter' });
  }

  const tableName = `stand_table_remaining${regime}`;

  try {
    const [results] = await db.query(`SELECT * FROM ??`, [tableName]);
    res.json(results);
  } catch (error) {
    console.error('Error fetching remaining:', error);
    res.status(500).json({ error: 'Failed to fetch stand table remaining data' });
  }
});

app.get('/api/stand-table-general', async (req, res) => {
  const regime = req.query.regime;

  if (!regime || !['45', '50', '55', '60', '65'].includes(regime)) {
    return res.status(400).json({ error: 'Invalid or missing regime parameter' });
  }

  const tableName = `stand_table_general${regime}`;

  try {
    const [rows] = await db.query(`SELECT * FROM ??`, [tableName]);
    res.json(rows);
  } catch (err) {
    console.error('Error fetching stand table general data:', err);
    res.status(500).json({ error: 'Database query failed' });
  }
});

app.get('/api/stand-table-production30', async (req, res) => {
  const regime = req.query.regime;

  if (!regime || !['45', '50', '55', '60', '65'].includes(regime)) {
    return res.status(400).json({ error: 'Invalid or missing regime parameter' });
  }

  const tableName = `stand_table_production30_${regime}`;

  try {
    const [rows] = await db.query(`SELECT * FROM ??`, [tableName]);
    res.json(rows);
  } catch (err) {
    console.error('Error fetching stand table production 30-year data:', err);
    res.status(500).json({ error: 'Database query failed' });
  }
});

const PORT = 5000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
