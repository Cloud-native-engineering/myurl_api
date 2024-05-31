from app.restrictions import bp
from app.extensions import db
from app.models.restriction import Restriction, RestrictionIn, RestrictionOut, RestrictionBlacklistOut, RestrictionPremiumOut
from app.security.guards import authorization_guard, permissions_guard, admin_permissions

####
## view functions
####
@bp.get('/<int:restriction_id>')
@bp.output(RestrictionOut)
@bp.doc(security='bearerAuth')
@authorization_guard
@permissions_guard([admin_permissions.read])
def get_restriction(restriction_id: int):
    return db.get_or_404(Restriction, restriction_id)

@bp.get('/')
@bp.output(RestrictionOut(many=True))
@bp.doc(security='bearerAuth')
@authorization_guard
@permissions_guard([admin_permissions.read])
def get_restrictions():
    return Restriction.query.all()

@bp.get('/blacklisted')
@bp.output(RestrictionBlacklistOut)
@bp.doc(security='bearerAuth')
@authorization_guard
def get_blacklisted_restrictions():
    blacklisted_restrictions = Restriction.query.filter_by(is_blacklisted=True).all()
    short_urls = [r.short_url for r in blacklisted_restrictions if r.short_url is not None]
    domains = [r.domain for r in blacklisted_restrictions if r.domain is not None]
    return {'short_urls': short_urls, 'domains': domains}

@bp.get('/premium')
@bp.output(RestrictionPremiumOut)
@bp.doc(security='bearerAuth')
@authorization_guard
def get_premium_restrictions():
    blacklisted_restrictions = Restriction.query.filter_by(is_premium=True).all()
    short_urls = [r.short_url for r in blacklisted_restrictions if r.short_url is not None]
    domains = [r.domain for r in blacklisted_restrictions if r.domain is not None]
    return {'short_urls': short_urls, 'domains': domains}

@bp.post('/')
@bp.input(RestrictionIn)
@bp.output(RestrictionOut)
@bp.doc(security='bearerAuth')
@authorization_guard
@permissions_guard([admin_permissions.write])
def create_restriction(json_data: dict):
    restriction = Restriction(**json_data)
    db.session.add(restriction)
    db.session.commit()
    return restriction

@bp.patch('/<int:restriction_id>')
@bp.input(RestrictionIn(partial=True))
@bp.output(RestrictionOut)
@bp.doc(security='bearerAuth')
@authorization_guard
@permissions_guard([admin_permissions.write])
def update_restriction(restriction_id: int, json_data: dict):
    restriction = db.get_or_404(Restriction, restriction_id)
    for attr, value in json_data.items():
        setattr(restriction, attr, value)
    db.session.commit()
    return restriction

@bp.delete('/<int:restriction_id>')
@bp.output({}, status_code=204)
@bp.doc(security='bearerAuth')
@authorization_guard
@permissions_guard([admin_permissions.write])
def delete_restriction(restriction_id: int):
    restriction = db.get_or_404(Restriction, restriction_id)
    db.session.delete(restriction)
    db.session.commit()
    return None

