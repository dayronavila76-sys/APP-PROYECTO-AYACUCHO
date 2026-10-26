from app.config.database import connect

ALLOWED={'cultura','naturaleza','gastronomia','aventura'}

def generate_itinerary(days, budget, interests, db_path=None):
    if type(days) is not int or not 1<=days<=14:
        raise ValueError('Los días deben estar entre 1 y 14.')
    if isinstance(budget,bool) or not isinstance(budget,(int,float)) or not 0<budget<=1000000:
        raise ValueError('El presupuesto debe ser un número positivo y válido.')
    interests=set(interests)
    if not interests or not interests.issubset(ALLOWED):
        raise ValueError('Selecciona al menos un interés válido.')
    with connect(db_path) as db:
        rows=db.execute('SELECT * FROM atractivos ORDER BY costo, id').fetchall()
        choices=[r for r in rows if r['interes'] in interests]
        remaining=float(budget)
        selections=[]
        capacities=[8]*days
        for place in choices:
            if place['costo']>remaining: continue
            day=next((i for i,free in enumerate(capacities) if free>=place['duracion']),None)
            if day is None: continue
            capacities[day]-=place['duracion']
            remaining-=place['costo']
            selections.append({'id':place['id'],'nombre':place['nombre'],'interes':place['interes'],
                               'costo':place['costo'],'duracion':place['duracion'],'dia':day+1})
        if not selections:
            raise ValueError('No hay atractivos compatibles. Modifica presupuesto o intereses.')
        total=round(float(budget)-remaining,2)
        cur=db.execute('INSERT INTO itinerarios(dias,presupuesto,intereses,costo_estimado) VALUES(?,?,?,?)',
                       (days,float(budget),','.join(sorted(interests)),total))
        for place in selections:
            db.execute('INSERT INTO itinerario_detalle(itinerario_id,atractivo_id,dia) VALUES(?,?,?)',
                       (cur.lastrowid,place['id'],place['dia']))
        return {'id':cur.lastrowid,'dias':days,'presupuesto':round(float(budget),2),
                'costo':total,'saldo':round(remaining,2),'lugares':selections}
