// React
import { Link } from "react-router-dom"

// Third Party
import { BaseSectionHeader } from "aa-geuthur-react";
import { Card } from "react-bootstrap";

function MainPage() {
	return (
		<Card className="border-0 bg-transparent">
			<BaseSectionHeader />
			<Card className="mt-3 bg-dark border-secondary">
				<Card.Body>
					<div className="d-flex align-items-center justify-content-between gap-3">
						<span>Example Content</span>
						<Link className="btn btn-sm btn-outline-light" to="styleguide/">
							Style Guide
						</Link>
					</div>
				</Card.Body>
			</Card>
		</Card>
	);
}

export default MainPage
