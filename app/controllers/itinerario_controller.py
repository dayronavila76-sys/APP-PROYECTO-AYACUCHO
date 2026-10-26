from app.models.itinerario import generate_itinerary, ALLOWED

def submit(form, db_path=None):
    try:
        day_value=str(form.get('dias','')).strip()
        days=int(day_value)
        if str(days)!=day_value: raise ValueError()
    except (ValueError,TypeError):
        raise ValueError('Los días deben ser un número entero entre 1 y 14.')
    try:
        budget=float(str(form.get('presupuesto','')).strip())
    except (ValueError,TypeError):
        raise ValueError('Ingresa un presupuesto numérico.')
    raw=form.get('intereses',[])
    if isinstance(raw,str): raw=[raw]
    interests=[x for x in raw if x in ALLOWED]
    if len(interests)!=len(raw): raise ValueError('Hay un interés no permitido.')
    return generate_itinerary(days,budget,interests,db_path)
